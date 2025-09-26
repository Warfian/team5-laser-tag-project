# network.py
# j.t. wood
# description: this file creates a udp server that 
# broadcasts on port 7500 and listens on port 7501. 
#
# last updated: 25Sep2025

import socket
import threading
import queue

BROADCAST_PORT = 7500
RECEIVE_PORT   = 7501
broadcast_addr = "127.0.0.1"
buffer_size    = 1024
incoming_q     = queue.Queue()

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

# start_listening() may need change pursuant to sprint 3 needs
def start_listening (r_sock, q):
    def collect_packet ():
        while True:
            data, addr = r_sock.recvfrom(buffer_size)
            q.put(format(data), addr)
    # threading listens in background without blocking
    thread = threading.Thread(target = collect_packet, daemon = True)
    thread.start()

def change_broadcast_ip (new_addr):
    global broadcast_addr
    broadcast_addr = new_addr
    return
