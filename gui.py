import os, queue, time
import tkinter as tk
from chat_initiator import show_history, display_users, start_chat

class Gui:
    def __init__(self, peers, recv_queue):
        self.peers = peers
        self.recv_queue = recv_queue

        self.chat_conversations = load_chat_history()
        self.current_chat = None
        self.username = None

        # Setup main window
        self.root = tk.Tk()
        self.root.title("Packet Sniffers")
        self.root.geometry("700x450")

        # 1) TOP BAR
        top_bar = tk.Frame(self.root, bg="#f0f0f0", height=40)
        top_bar.pack(side=tk.TOP, fill=tk.X)

        self.secured_var = tk.BooleanVar(value=False)
        secured_switch = tk.Checkbutton(
            top_bar,
            text="Secured",
            variable=self.secured_var,
            onvalue=True,
            offvalue=False,
            relief=tk.RAISED,
            indicatoron=False,
            width=10,
            font=("Arial", 12),
            cursor="hand2"
        )
        secured_switch.pack(side=tk.RIGHT, padx=5, pady=5)

        history_button = tk.Button(
            top_bar,
            text="History",
            command=show_history,
            font=("Arial", 12)
        )
        history_button.pack(side=tk.RIGHT, padx=5, pady=5)

        users_button = tk.Button(
            top_bar,
            text="Users",
            command=lambda: display_users(self.peers),
            font=("Arial", 12)
        )
        users_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # 2) MAIN CONTENT FRAME
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.grid_columnconfigure(0, weight=0)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # 3) USER PANEL
        user_panel = tk.Frame(main_frame, bg="#ffffff", bd=1, relief=tk.SOLID)
        user_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 1))
        user_panel.grid_rowconfigure(1, weight=1)
        user_panel.grid_columnconfigure(0, weight=1)

        user_title = tk.Label(
            user_panel,
            text="Online Users",
            bg="#ffffff",
            fg="#00c000",
            font=("Courier", 16, "bold")
        )
        user_title.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        list_frame = tk.Frame(user_panel, bg="#ffffff")
        list_frame.grid(row=1, column=0, sticky="nsew")
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        user_scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        user_scrollbar.grid(row=0, column=1, sticky="ns")

        self.user_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=user_scrollbar.set,
            font=("Courier", 15, "bold")
        )
        self.user_listbox.grid(row=0, column=0, sticky="nsew")
        user_scrollbar.config(command=self.user_listbox.yview)

        self.user_listbox.bind("<<ListboxSelect>>", self.switch_chat)
        self.update_user_list()

        # 4) CHAT CONTAINER
        chat_container = tk.Frame(main_frame, bg="#ffffff", bd=1, relief=tk.SOLID)
        chat_container.grid(row=0, column=1, sticky="nsew")
        chat_container.grid_rowconfigure(0, weight=0)
        chat_container.grid_rowconfigure(1, weight=1)
        chat_container.grid_rowconfigure(2, weight=0)
        chat_container.grid_columnconfigure(0, weight=1)

        self.chat_header = tk.Label(
            chat_container,
            text="Select a user to chat",
            bg="#e0e0e0",
            fg="#000000",
            font=("Arial", 12, "bold")
        )
        self.chat_header.grid(row=0, column=0, sticky="ew")

        chat_frame = tk.Frame(chat_container, bg="#ffffff")
        chat_frame.grid(row=1, column=0, sticky="nsew")
        chat_frame.grid_rowconfigure(0, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)

        self.chat_text = tk.Text(
            chat_frame,
            state='disabled',
            wrap='word',
            font=("Arial", 13)
        )
        self.chat_text.grid(row=0, column=0, sticky="nsew")

        bottom_frame = tk.Frame(chat_container, bg="#f0f0f0", height=30)
        bottom_frame.grid(row=2, column=0, sticky="ew")

        self.message_entry = tk.Entry(bottom_frame, font=("Arial", 12))
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        send_button = tk.Button(
            bottom_frame,
            text="Send",
            command=self.send_message,
            font=("Arial", 12)
        )
        send_button.pack(side=tk.RIGHT, padx=5, pady=5)


        self.root.after(100, self._poll_incoming)
        self.root.mainloop()


    def _poll_incoming(self):
        """Poll the recv_queue and display any new messages."""
        while True:
            try:
                username, text, secured = self.recv_queue.get_nowait()
            except queue.Empty:
                break

            time_str = time.strftime("[%H:%M] ", time.localtime())
            prefix = "(Encrypted): " if secured else "(Unencrypted): "
            new_msg = f"{time_str}{username}: {prefix}{text}\n"
            self.chat_conversations.setdefault(username, "")
            self.chat_conversations[username] += new_msg

            if self.current_chat == username:
                self.chat_text.config(state='normal')
                self.chat_text.insert(tk.END, new_msg)
                self.chat_text.config(state='disabled')
                self.chat_text.see(tk.END)

        self.root.after(100, self._poll_incoming)


    def switch_chat(self, event):
        """Switch the active chat based on the selected user."""
        sel = self.user_listbox.curselection()
        if not sel:
            return
        entry = self.user_listbox.get(sel[0])
        self.current_chat = entry.split(" - ")[0]
        self.chat_header.config(text=f"Chat with {self.current_chat}")

        self.chat_text.config(state='normal')
        self.chat_text.delete(1.0, tk.END)
        if self.current_chat in self.chat_conversations:
            self.chat_text.insert(tk.END, self.chat_conversations[self.current_chat])
        self.chat_text.config(state='disabled')


    def send_message(self):
        """Send a message in the active chat."""
        msg = self.message_entry.get().strip()
        if not self.current_chat or not msg:
            return
        secured = self.secured_var.get()
        start_chat(peers=self.peers, username=self.current_chat, message=msg, secured=secured)

        time_str = time.strftime("[%H:%M] ", time.localtime())
        prefix = "(Encrypted): " if secured else "(Unencrypted): "
        new_msg = f"{time_str}You {prefix}{msg}\n"
        self.chat_conversations.setdefault(self.current_chat, "")
        self.chat_conversations[self.current_chat] += new_msg

        self.chat_text.config(state='normal')
        self.chat_text.insert(tk.END, new_msg)
        self.chat_text.config(state='disabled')
        self.chat_text.see(tk.END)
        self.message_entry.delete(0, tk.END)


    def update_user_list(self):
        """Refresh the user list every 3 seconds."""
        self.user_listbox.delete(0, tk.END)
        now = time.time()
        for ip, info in list(self.peers.items()):
            age = now - info.get("last_seen", 0)
            if age > 900:
                continue
            status = "Online" if age <= 10 else "Away"
            self.user_listbox.insert(tk.END, f"{info['username']} - {status}")
        self.root.after(3000, self.update_user_list)


def load_chat_history(log_file="chat_history.log"):
    """
    Parse the log file and build a dict of conversations by username.
    Returns {username: conversation_string}
    """
    history = {}
    if not os.path.exists(log_file):
        return history

    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                # Split into exactly 4 parts, so any extra " - " in the message won't break us
                # parts: [timestamp, "username (ip)", direction, "(Encrypted)/(Unencrypted): message"]
                parts = line.strip().split(' - ', 3)
                if len(parts) < 4:
                    continue

                timestamp_str, user_ip, direction, secure_and_msg = parts

                # Extract just the HH:MM from "YYYY-MM-DD HH:MM:SS"
                time_only = timestamp_str.split(' ')[1][:5]

                # Extract username
                username = user_ip.split(' (')[0]

                # Split off the "(Encyrpted)" or "(Unencrypted)" label
                if ': ' in secure_and_msg:
                    secure_label, msg = secure_and_msg.split(': ', 1)
                else:
                    secure_label, msg = '', secure_and_msg

                # Prepare the history bucket
                history.setdefault(username, '')

                # Build the line prefix
                prefix = f"[{time_only}] "
                if direction.upper() == 'SENT':
                    history[username] += f"{prefix}You {secure_label}: {msg}\n"
                elif direction.upper() == 'RECEIVED':
                    history[username] += f"{prefix}{username} {secure_label}: {msg}\n"

    except Exception as e:
        print(f"Failed to load chat history: {e}")

    return history
