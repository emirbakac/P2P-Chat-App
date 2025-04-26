import threading
from queue import Queue
from gui import Gui
from tkinter import simpledialog
from service_announcer import ServiceAnnouncer
from peer_discovery import PeerDiscovery
from chat_responder import ChatResponder

def main():
    username = simpledialog.askstring("~", "Enter your username: ")

    peers = {}
    recv_queue = Queue()

    announcer = ServiceAnnouncer(username)
    discovery = PeerDiscovery(peers)
    responder = ChatResponder(peers, recv_queue)

    for target in (announcer.start_broadcast, discovery.listen, responder.start_server):
        t = threading.Thread(target=target, daemon=True)
        t.start()

    gui = Gui(peers=peers, recv_queue=recv_queue)

if __name__ == "__main__":
    main()
