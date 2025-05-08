import time

def log_message(direction, username, ip, message, secured):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {username} ({ip}) - {direction} - {secured}: {message}\n"
    with open("chat_history.log", "a") as f:
        f.write(log_entry)

def display_users(peers):
    current_time = time.time()
    print("Available Users:")
    # Only display users seen in the last 15 minutes
    for ip, info in peers.items():
        # Filter out users not seen within the last 900 seconds
        if current_time - info["last_seen"] <= 900:
            status = "(Online)" if current_time - info["last_seen"] <= 10 else "(Away)"
            print(f"{info['username']} {status} - {ip}")

def show_history():
    try:
        with open("chat_history.log", "r") as log_file:
            print("\n--- Chat History ---")
            print(log_file.read())
            print("--------------------\n")
    except FileNotFoundError:
        print("No chat history found.")

def encrypt_message(message: str, key: int) -> str:
    """
    Mesajı önce UTF-8 bayt dizisine çevir, ardından her baytı key ile XOR et,
    sonucu hex string olarak döndür.
    """
    b = message.encode('utf-8')
    encrypted_bytes = bytes([byte ^ key for byte in b])
    return encrypted_bytes.hex()

def decrypt_message(encrypted_hex: str, key: int) -> str:
    """
    Hex string olarak gelen veriyi bayt dizisine çevir,
    her baytı key ile XOR’la, sonra UTF-8'e decode et.
    """
    encrypted_bytes = bytes.fromhex(encrypted_hex)
    decrypted_bytes = bytes([byte ^ key for byte in encrypted_bytes])
    return decrypted_bytes.decode('utf-8')
