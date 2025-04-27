import json, random

# Public parameters
P = 19  # Prime modulus
G = 2   # Generator

def generate_private_key():
    return random.randint(1, P - 2)


def compute_public_key(private_key):
    return pow(G, private_key, P)


def compute_shared_key(their_public, my_private):
    return pow(their_public, my_private, P)


def perform_diffie_hellman(socket_obj):
    # generate keys
    my_private = generate_private_key()
    my_public = compute_public_key(my_private)

    # send your public key wrapped in JSON
    msg_out = json.dumps({"key": str(my_public)})
    socket_obj.sendall(msg_out.encode())

    # wait for the peer's public key
    data = socket_obj.recv(1024)
    their_msg = json.loads(data.decode())
    their_public = int(their_msg.get("key"))

    # compute shared secret
    shared_key = compute_shared_key(their_public, my_private)
    return shared_key