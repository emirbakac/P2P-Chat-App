from diffie_hellman import generate_private_key, compute_public_key, compute_shared_key
from utils import encrypt_message, decrypt_message

#karşı taraf ı yı algılamadığı için (ı 1 oldu) utilsi hexlik değiştirdik (ı 4e sığmadı) şuan testi geçiyo
def main():
    # iki taraf için rasgele private/public anahtarları
    priv_a = generate_private_key()
    pub_a  = compute_public_key(priv_a)

    priv_b = generate_private_key()
    pub_b  = compute_public_key(priv_b)

    # ortak anahtarı her iki tarafta da hesaplayalım
    shared_a = compute_shared_key(pub_b, priv_a)
    shared_b = compute_shared_key(pub_a, priv_b)

    print(f"[1] Shared key at A: {shared_a}")
    print(f"[2] Shared key at B: {shared_b}")

    # anahtarların eşit olup olmadığını test edelim
    if shared_a != shared_b:
        print("Diffie–Hellman FAILED: Anahtarlar farklı!")
        return
    print("Diffie–Hellman OK: Anahtarlar eşit.")

    # şimdi bir mesajı şifreleyip diğer tarafta çözelim
    original_msg = "Merhaba, bu secure test mesajıdır!"
    encrypted = encrypt_message(original_msg, shared_a)
    decrypted = decrypt_message(encrypted, shared_b)

    print(f"[3] Orijinal mesaj: {original_msg}")
    print(f"[4] Şifreli hâl : {encrypted!r}")
    print(f"[5] Çözülmüş hâl: {decrypted}")

    # mesajın doğru çevrilip çevrilmediğini kontrol edelim
    if decrypted == original_msg:
        print("Encryption/Decryption OK: Mesaj eksiksiz geri alındı.")
    else:
        print("Encryption/Decryption FAILED: Mesaj farklı!")

if __name__ == "__main__":
    main()