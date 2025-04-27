import time

def log_message(direction, username, ip, message, secured):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {username} ({ip}) - {direction} - {secured}: {message}\n"
    with open("chat_history.log", "a") as f:
        f.write(log_entry)

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
