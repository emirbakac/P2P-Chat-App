# Example Diffie-Hellman key exchange functions with p = 19 and g = 2
import json
import random

P = 19
G = 2

def generate_private_key():
    # For demonstration, choose a small random private key.
    return random.randint(1, P - 2)


def compute_public_key(private_key):
    return pow(G, private_key, P)


def compute_shared_key(their_public, my_private):
    return pow(their_public, my_private, P)


def perform_diffie_hellman(socket_obj):
    # This function handles a simplified Diffie-Hellman exchange over a TCP socket.
    my_private = generate_private_key()
    my_public = compute_public_key(my_private)

    # Send your public key wrapped in a JSON message.
    socket_obj.sendall(f'{{"key": "{my_public}"}}'.encode())

    # Wait for the other party's public key.
    data = socket_obj.recv(1024)
    their_msg = json.loads(data.decode())
    their_public = int(their_msg.get("key"))

    shared_key = compute_shared_key(their_public, my_private)
    return shared_key
