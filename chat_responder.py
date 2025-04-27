import socket, json, threading
from diffie_hellman import generate_private_key, compute_public_key, compute_shared_key
from utils import log_message, decrypt_message

TCP_PORT = 6001

class ChatResponder:
    def __init__(self, peers, recv_queue):
        self.peers = peers
        self.recv_queue = recv_queue

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("", TCP_PORT))
        server.listen(5)
        while True:
            client_sock, addr = server.accept()
            threading.Thread(target=self.handle_client, args=(client_sock, addr), daemon=True).start()

    def handle_client(self, client_sock, addr):
        with client_sock:
            try:
                data = client_sock.recv(4096)
                if not data:
                    return
                message = json.loads(data.decode())
                sender_ip = addr[0]
                sender_username = self.peers.get(sender_ip, {}).get("username", sender_ip)

                # Diffie‐Hellman key exchange:
                if "key" in message:
                    # karşı tarafın public’ini al
                    their_public = int(message["key"])
                    # kendi private/public’ini üret
                    my_private = generate_private_key()
                    my_public = compute_public_key(my_private)
                    # sunucu public’ini gönder
                    client_sock.sendall(
                        json.dumps({"key": str(my_public)}).encode()
                    )
                    # ortak anahtarı hesapla
                    shared_key = compute_shared_key(their_public, my_private)

                    # ardından gerçek sohbet mesajını oku
                    data = client_sock.recv(4096)
                    if not data:
                        return
                    message = json.loads(data.decode())
                else:
                    shared_key = None

                # Encrypted text:
                if "encryptedmessage" in message:
                    text = decrypt_message(message["encryptedmessage"], shared_key)
                    log_message("RECEIVED", sender_username, sender_ip, text, "(Encrypted)")
                    self.recv_queue.put((sender_username, text, True))
                # Plain text:
                elif "unencryptedmessage" in message:
                    text = message["unencryptedmessage"]
                    log_message("RECEIVED", sender_username, sender_ip, text, "(Unencrypted)")
                    self.recv_queue.put((sender_username, text, False))
                else:
                    print("Unknown message format received.")
            except Exception as e:
                print("ChatResponder error:", e)
