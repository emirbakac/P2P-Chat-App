import time

def log_message(direction, username, ip, message, secured):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {username} ({ip}) - {direction} - {secured}: {message}\n"
    with open("chat_history.log", "a") as f:
        f.write(log_entry)

def encrypt_message(message, key):
    # For demonstration, use a simple reversible operation (do not use in production)
    # You can replace this with a proper encryption method from a library like cryptography.
    encrypted = ''.join(chr((ord(char) + key) % 256) for char in message)
    return encrypted

def decrypt_message(encrypted_message, key=None):
    # If the key is known, reverse the encryption; for demonstration, assume a preset key if not provided.
    if key is None:
        # This is just a placeholder; in secure chat, the shared key would be used.
        key = 5
    decrypted = ''.join(chr((ord(char) - key) % 256) for char in encrypted_message)
    return decrypted
