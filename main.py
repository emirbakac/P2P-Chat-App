import threading
from gui import Gui
from tkinter import simpledialog
from service_announcer import ServiceAnnouncer
from peer_discovery import PeerDiscovery
from chat_responder import ChatResponder
from chat_initiator import chat_menu

def main():
    # Ask for username at startup (used by ServiceAnnouncer)
    username = simpledialog.askstring("~", "Enter your username: ")

    # Shared dictionary for peers {ip: {"username": str, "last_seen": timestamp}}
    peers = {}

    # Initialize threads for UDP broadcasting and listening and TCP response.
    announcer = ServiceAnnouncer(username)
    discovery = PeerDiscovery(peers)
    responder = ChatResponder(peers)

    # Start background services in separate threads.
    service_threads = [
        threading.Thread(target=announcer.start_broadcast, daemon=True),
        threading.Thread(target=discovery.listen, daemon=True),
        threading.Thread(target=responder.start_server, daemon=True)
    ]

    for thread in service_threads:
        thread.start()

    # Run the GUI in the main thread.
    gui = Gui(peers)  # This calls mainloop() and will block the main thread.

if __name__ == "__main__":
    main()
