import socket, json, time

LISTEN_PORT = 6000

class PeerDiscovery:
    def __init__(self, peers):
        self.peers = peers

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(("", LISTEN_PORT))
            while True:
                try:
                    data, addr = sock.recvfrom(1024)
                    message = json.loads(data.decode())
                    username = message.get("username")
                    ip = addr[0]
                    self.peers[ip] = {"username": username, "last_seen": time.time()}
                    print(f"{username} is online from IP {ip}")
                except Exception as e:
                    print("PeerDiscovery error:", e)
