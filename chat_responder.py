import socket, json, threading
from diffie_hellman import perform_diffie_hellman
from utils import log_message, decrypt_message

TCP_PORT = 6001

class ChatResponder:
    def __init__(self, peers, recv_queue):
        self.peers = peers
        self.recv_queue = recv_queue

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(("", TCP_PORT))
            server.listen(5)
            while True:
                client_sock, addr = server.accept()
                threading.Thread(target=self.handle_client,args=(client_sock, addr),daemon=True).start()

    def handle_client(self, client_sock, addr):
        with client_sock:
            try:
                data = client_sock.recv(1024)
                if not data:
                    return
                message = json.loads(data.decode())
                sender_ip = addr[0]
                sender_username = self.peers.get(sender_ip, {}).get("username", sender_ip)

                # Diffie‐Hellman key exchange:
                if "key" in message:
                    perform_diffie_hellman(client_sock)
                # Encrypted text:
                elif "encryptedmessage" in message:
                    text = decrypt_message(message["encryptedmessage"])
                    log_message("RECEIVED", sender_username, sender_ip, text)
                    self.recv_queue.put((sender_username, text, True))
                # Plain text:
                elif "unencryptedmessage" in message:
                    text = message["unencryptedmessage"]
                    log_message("RECEIVED", sender_username, sender_ip, text)
                    self.recv_queue.put((sender_username, text, False))
                else:
                    print("Unknown message format received.")
            except Exception as e:
                print("ChatResponder error:", e)
