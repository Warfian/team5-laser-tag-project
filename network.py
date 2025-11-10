# network.py
# j.t. wood
# description: this file creates a udp server that 
# broadcasts on port 7500 and listens on port 7501
# in order to handle game events.
# last updated: 6Nov2025

import socket
import threading
import queue
import time
import gamescreen
import music

BROADCAST_PORT = 7500
RECEIVE_PORT   = 7501
broadcast_addr = "127.0.0.1"
buffer_size    = 1024
incoming_q     = queue.Queue()
listening      = False
processing     = False

def setup_broadcast_socket (ip = broadcast_addr, port = BROADCAST_PORT):
    b_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    b_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return b_sock, (ip, port)

def setup_receive_socket (port = RECEIVE_PORT):
    r_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    r_sock.bind(("0.0.0.0", port))
    return r_sock

# socket init
broadcast_sock, broadcast_addr_port = setup_broadcast_socket(broadcast_addr, BROADCAST_PORT)
recv_sock = setup_receive_socket(RECEIVE_PORT)

def start_listening (r_sock, q):
    global listening
    def collect_packet ():
        while True:
            data, addr = r_sock.recvfrom(buffer_size)
            q.put((data.decode().strip()))
    if not listening:
        thread = threading.Thread(target = collect_packet, daemon = True)
        thread.start()
        listening = True

def change_broadcast_ip (new_addr):
    global broadcast_addr
    broadcast_addr = new_addr
    return

def broadcast_game_start():
    start_code = 202
    broadcast_sock.sendto(str(start_code).encode('utf-8'), broadcast_addr_port)

def broadcast_game_end(): # 3x
    end_code = 221
    for i in range(3):
        broadcast_sock.sendto(str(end_code).encode('utf-8'), broadcast_addr_port)
        time.sleep(0.1)

def process_messages(q):
    # green - even
    # red   - odd
    msg_received = False
    try:
        msg = q.get_nowait()
        msg_received = True
    except queue.Empty:
        pass

    if msg_received:
        sender_id, target_id = msg.split(":")
        sender_id_num = int(sender_id)
        target_id_num = int(target_id)
        
        # for friendly fire, sum is always even; (odd+odd or even+even)
        sum = sender_id_num + target_id_num 
        even_sum = (sum % 2 == 0)
        
        if target_id_num == 53:
            # base score (red)
            player_is_green = (sender_id_num % 2 == 0)
            if player_is_green:
                broadcast_sock.sendto(str.encode(target_id), broadcast_addr_port)
                gamescreen.handle_base_hit("red", sender_id_num)
            music.play_base()
        
        elif target_id_num == 43:
            # base score (green)
            player_is_red = (sender_id_num % 2 != 0)
            if player_is_red:
                broadcast_sock.sendto(str.encode(target_id), broadcast_addr_port)
                gamescreen.handle_base_hit("green", sender_id_num)
            music.play_base()
        
        elif even_sum: 
            # friendly fire
            broadcast_sock.sendto(str.encode(sender_id), broadcast_addr_port)
            broadcast_sock.sendto(str.encode(target_id), broadcast_addr_port)
            gamescreen.handle_score_event(sender_id_num, "sub")
            gamescreen.handle_score_event(target_id_num, "sub")
            music.play_friendly_fire()
        
        elif not even_sum:
            # unfriendly fire
            broadcast_sock.sendto(str.encode(target_id), broadcast_addr_port)
            gamescreen.handle_score_event(sender_id_num, "add")
            music.play_hit()
        
        else: 
            pass

def start_processing (): # for testing only
    global processing
    def processor_thread(q):
        while True:
            process_messages(q)
            time.sleep(0.1)
    if not processing:
        thread = threading.Thread(target=processor_thread, args=(incoming_q,), daemon=True)
        thread.start()
        processing = True






def main():
    # socket init
    # broadcast_sock, broadcast_addr_port = setup_broadcast_socket(broadcast_addr, BROADCAST_PORT)
    # recv_sock = setup_receive_socket(RECEIVE_PORT)
    
    start_listening(recv_sock, incoming_q)
    # print(f"broadcast_sock:{broadcast_sock}\nbroadcast_addr_port:{broadcast_addr_port}\nrecv_sock:{recv_sock}")
    start_processing()



if __name__ == "__main__":  
    # main()

    print("=== NETWORK.PY TEST INTERFACE ===")
    print(f"listening on port {RECEIVE_PORT}")
    print(f"broadcasting on port {BROADCAST_PORT}")
    print("press ctrl+c to exit.\n")

    # Start the listener thread
    start_listening(recv_sock, incoming_q)

    # for testing - start the queue processor in a separate thread
    start_processing()

    menu = (
        "commands:\n"
        "1 - broadcast game start (202)\n"
        "2 - broadcast game end   (221)\n"
        "3 - change broadcast ip\n"
        "0 - quit\n"
        "> "
    )

    try:
        while True:
            choice = input(menu).strip()

            if choice == "1":
                broadcast_game_start()
            elif choice == "2":
                broadcast_game_end()
            elif choice == "3":
                new_ip = input("enter new broadcast ip: ").strip()
                change_broadcast_ip(new_ip)
                print(f"broadcast ip updated to {broadcast_addr}")
            elif choice == "0":
                print("exiting test interface.")
                break
            else:
                print("invalid choice.")

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nexiting test interface.")