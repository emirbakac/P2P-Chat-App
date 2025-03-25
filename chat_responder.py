import socket
import json
import threading
from diffie_hellman import perform_diffie_hellman
from utils import log_message, decrypt_message

TCP_PORT = 6001

class ChatResponder:
    def __init__(self, peers):
        self.peers = peers

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(("", TCP_PORT))
            server.listen(5)
            print("ChatResponder is listening on port", TCP_PORT)
            while True:
                client_sock, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client_sock, addr), daemon=True).start()

    def handle_client(self, client_sock, addr):
        with client_sock:
            try:
                data = client_sock.recv(1024)
                if not data:
                    return
                message = json.loads(data.decode())
                sender_ip = addr[0]
                sender_username = self.peers.get(sender_ip, {}).get("username", sender_ip)

                if "key" in message:
                    # Secure chat: complete Diffie-Hellman exchange.
                    shared_key = perform_diffie_hellman(client_sock)
                    # The rest of the secure exchange would follow...
                elif "encryptedmessage" in message:
                    decrypted = decrypt_message(message["encryptedmessage"])
                    print(f"{sender_username}: {decrypted}")
                    log_message("RECEIVED", sender_username, sender_ip, decrypted)
                elif "unencryptedmessage" in message:
                    print(f"{sender_username}: {message['unencryptedmessage']}")
                    log_message("RECEIVED", sender_username, sender_ip, message["unencryptedmessage"])
                else:
                    print("Unknown message format received.")
            except Exception as e:
                print("ChatResponder error:", e)
