import threading
from service_announcer import ServiceAnnouncer
from peer_discovery import PeerDiscovery
from chat_responder import ChatResponder
from chat_initiator import chat_menu

def main():
    # Ask for username at startup (used by ServiceAnnouncer)
    username = input("Enter your username: ")

    # Shared dictionary for peers {ip: {"username": str, "last_seen": timestamp}}
    peers = {}

    # Initialize threads for UDP broadcasting and listening and TCP response.
    announcer = ServiceAnnouncer(username)
    discovery = PeerDiscovery(peers)
    responder = ChatResponder(peers)

    # Start background services in separate threads.
    threads = [
        threading.Thread(target=announcer.start_broadcast, daemon=True),
        threading.Thread(target=discovery.listen, daemon=True),
        threading.Thread(target=responder.start_server, daemon=True)
    ]

    for t in threads:
        t.start()

    # Start the Chat Initiator (CLI) loop in the main thread.
    chat_menu(peers)

if __name__ == "__main__":
    main()
