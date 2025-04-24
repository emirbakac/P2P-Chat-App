import tkinter as tk
from chat_initiator import show_history, display_users

class Gui:
    def __init__(self, peers):
        # Instance attributes for chat state
        self.chat_conversations = {}
        self.current_chat = None

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

        history_button = tk.Button(top_bar, text="History", command=show_history, font=("Arial", 12))
        history_button.pack(side=tk.RIGHT, padx=5, pady=5)
        users_button = tk.Button(top_bar, text="Users", command=lambda: display_users(peers), font=("Arial", 12))
        users_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # 2) MAIN CONTENT FRAME (split into left user list and right chat container)
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.grid_columnconfigure(0, weight=0)  # User list column (fixed)
        main_frame.grid_columnconfigure(1, weight=1)  # Chat container column (expand)
        main_frame.grid_rowconfigure(0, weight=1)

        # 3) USER PANEL (left side)
        user_panel = tk.Frame(main_frame, bg="#ffffff", bd=1, relief=tk.SOLID)
        user_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 1))
        user_panel.grid_rowconfigure(1, weight=1)
        user_panel.grid_columnconfigure(0, weight=1)

        user_title = tk.Label(user_panel, text="Online Users", bg="#ffffff", fg="#00c000",
                              font=("Courier", 16, "bold"))
        user_title.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Frame to hold the listbox and its scrollbar
        list_frame = tk.Frame(user_panel, bg="#ffffff")
        list_frame.grid(row=1, column=0, sticky="nsew")
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        user_scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        user_scrollbar.grid(row=0, column=1, sticky="ns")

        self.user_listbox = tk.Listbox(list_frame, yscrollcommand=user_scrollbar.set,
                                       font=("Courier", 15, "bold"))
        self.user_listbox.grid(row=0, column=0, sticky="nsew")
        user_scrollbar.config(command=self.user_listbox.yview)

        # Populate with example entries
        self.user_listbox.insert(tk.END, "emirbakac - Online")
        self.user_listbox.insert(tk.END, "eylul - Away")

        # Bind selection event to switch chat
        self.user_listbox.bind("<<ListboxSelect>>", self.switch_chat)

        # 4) CHAT CONTAINER (right side)
        chat_container = tk.Frame(main_frame, bg="#ffffff", bd=1, relief=tk.SOLID)
        chat_container.grid(row=0, column=1, sticky="nsew")
        chat_container.grid_rowconfigure(0, weight=0)  # Header row
        chat_container.grid_rowconfigure(1, weight=1)  # Chat display expands
        chat_container.grid_rowconfigure(2, weight=0)  # Message entry row
        chat_container.grid_columnconfigure(0, weight=1)

        # 4a) Chat Header
        self.chat_header = tk.Label(chat_container, text="Select a user to chat",
                                    bg="#e0e0e0", fg="#000000", font=("Arial", 12, "bold"))
        self.chat_header.grid(row=0, column=0, sticky="ew")

        # 4b) Chat Display Area
        chat_frame = tk.Frame(chat_container, bg="#ffffff")
        chat_frame.grid(row=1, column=0, sticky="nsew")
        chat_frame.grid_rowconfigure(0, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)

        self.chat_text = tk.Text(chat_frame, state='disabled', wrap='word', font=("Arial", 11))
        self.chat_text.grid(row=0, column=0, sticky="nsew")

        # 4c) Message Entry (only in chat_container)
        bottom_frame = tk.Frame(chat_container, bg="#f0f0f0", height=30)
        bottom_frame.grid(row=2, column=0, sticky="ew")

        self.message_entry = tk.Entry(bottom_frame, font=("Arial", 12))
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        send_button = tk.Button(bottom_frame, text="Send", command=self.send_message, font=("Arial", 12))
        send_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.root.mainloop()


    def switch_chat(self, event):
        """Switch the active chat based on the selected user in the listbox."""
        selection = self.user_listbox.curselection()
        if selection:
            # Extract username from the selected entry (assumes format "username - status")
            entry = self.user_listbox.get(selection[0])
            username = entry.split(" - ")[0]
            self.current_chat = username

            # Update the chat header label
            self.chat_header.config(text=f"Chat with {username}")

            # Load the conversation if it exists, or clear the chat area
            self.chat_text.config(state='normal')
            self.chat_text.delete(1.0, tk.END)
            if username in self.chat_conversations:
                self.chat_text.insert(tk.END, self.chat_conversations[username])
            self.chat_text.config(state='disabled')


    def send_message(self):
        """Send a message in the active chat conversation."""
        message = self.message_entry.get()
        if self.current_chat and message.strip():
            # Determine prefix based on secured switch
            prefix = "Secured: " if self.secured_var.get() else "Not Secured: "
            new_message = f"You: {prefix}{message}\n"

            # Append to the current chat conversation in the dictionary
            if self.current_chat in self.chat_conversations:
                self.chat_conversations[self.current_chat] += new_message
            else:
                self.chat_conversations[self.current_chat] = new_message

            # Display the new message in the chat area
            self.chat_text.config(state='normal')
            self.chat_text.insert(tk.END, new_message)
            self.chat_text.config(state='disabled')
            self.chat_text.see(tk.END)
            self.message_entry.delete(0, tk.END)

