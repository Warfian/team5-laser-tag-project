# udp_listener.py
import socket

BROADCAST_PORT = 7500
BUFFER_SIZE = 1024

# Listen on all interfaces
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock.bind(("0.0.0.0", BROADCAST_PORT))


print(f"listening on port {BROADCAST_PORT}...")


while True:
    data, addr = recv_sock.recvfrom(BUFFER_SIZE)
    print(f"Received from {addr}: {data.decode()}")
