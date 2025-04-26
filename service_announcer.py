import socket, json, time

BROADCAST_IP = "192.168.1.255"
BROADCAST_PORT = 6000

class ServiceAnnouncer:
    def __init__(self, username):
        self.username = username
        self.message = json.dumps({"username": self.username})
        self.broadcast_interval = 8  # seconds

    def start_broadcast(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            while True:
                try:
                    sock.sendto(self.message.encode(), (BROADCAST_IP, BROADCAST_PORT))
                    print(f"Broadcasted: {self.message}")
                except Exception as e:
                    print("Broadcast error:", e)
                time.sleep(self.broadcast_interval)
