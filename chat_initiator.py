import socket, json
from diffie_hellman import perform_diffie_hellman
from utils import log_message, encrypt_message

TCP_PORT = 6001

def start_chat(peers, username, message, secured):

    target_username = username

    # Find IP address for the given username from peers dictionary.
    target_ip = None
    for ip, info in peers.items():
        if info["username"] == target_username:
            target_ip = ip
            break

    if not target_ip:
        print("User not found in peer list.")
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target_ip, TCP_PORT))
            if  secured:
                shared_key = perform_diffie_hellman(s)
                encrypted = encrypt_message(message, shared_key)
                json_msg = json.dumps({"encryptedmessage": encrypted})
                log_message("SENT", target_username, target_ip, message, "(Encrypted)")
            else:
                json_msg = json.dumps({"unencryptedmessage": message})
                log_message("SENT", target_username, target_ip, message, "(Unencrypted)")
            s.sendall(json_msg.encode())

    except Exception as e:
        print("Error initiating chat:", e)
