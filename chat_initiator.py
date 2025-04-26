import socket, json, time
from diffie_hellman import perform_diffie_hellman
from utils import log_message, encrypt_message

TCP_PORT = 6001

def display_users(peers):
    current_time = time.time()
    print("Available Users:")
    # Only display users seen in the last 15 minutes
    for ip, info in peers.items():
        # Filter out users not seen within the last 900 seconds
        if current_time - info["last_seen"] <= 900:
            status = "(Online)" if current_time - info["last_seen"] <= 10 else "(Away)"
            print(f"{info['username']} {status} - {ip}")


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
                msg = message
                encrypted = encrypt_message(msg, shared_key)
                json_msg = json.dumps({"encryptedmessage": encrypted})
            else:
                msg = message
                json_msg = json.dumps({"unencryptedmessage": msg})
            s.sendall(json_msg.encode())
            log_message("SENT", target_username, target_ip, msg)
    except Exception as e:
        print("Error initiating chat:", e)

def show_history():
    try:
        with open("chat_history.log", "r") as log_file:
            print("\n--- Chat History ---")
            print(log_file.read())
            print("--------------------\n")
    except FileNotFoundError:
        print("No chat history found.")
