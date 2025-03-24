import socket
import json
import time
from diffie_hellman import perform_diffie_hellman
from utils import log_message, encrypt_message

TCP_PORT = 6001  # port to connect to remote ChatResponder


def chat_menu(peers):
    while True:
        choice = input("Enter command (Users / Chat / History): ").strip().lower()
        if choice == "users":
            display_users(peers)
        elif choice == "chat":
            start_chat(peers)
        elif choice == "history":
            show_history()
        else:
            print("Invalid command.")


def display_users(peers):
    current_time = time.time()
    print("Available Users:")
    for ip, info in peers.items():
        status = "(Online)" if current_time - info["last_seen"] <= 10 else "(Away)"
        print(f"{info['username']} {status} - {ip}")


def start_chat(peers):
    target_username = input("Enter the username to chat with: ").strip()
    secure_chat = input("Chat securely? (yes/no): ").strip().lower() == "yes"

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
            if secure_chat:
                # Begin Diffie-Hellman exchange
                # For simplicity, assume perform_diffie_hellman handles the exchange and returns a shared key.
                shared_key = perform_diffie_hellman(s)
                # Now let the user type a message, encrypt it, and send.
                msg = input("Enter your message: ")
                encrypted = encrypt_message(msg, shared_key)
                json_msg = json.dumps({"encryptedmessage": encrypted})
            else:
                msg = input("Enter your message: ")
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
