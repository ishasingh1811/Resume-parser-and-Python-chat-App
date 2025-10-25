import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

# ---------------- CLIENT SETUP ----------------
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

nickname = simpledialog.askstring("Nickname", "Enter your name:")

# ---------------- GUI SETUP ----------------
root = tk.Tk()
root.title("Chat App")

chat_area = scrolledtext.ScrolledText(root)
chat_area.pack(padx=20, pady=5)
chat_area.config(state='disabled')

msg_entry = tk.Entry(root, width=50)
msg_entry.pack(padx=20, pady=5)

def send_message(event=None):
    message = f"{nickname}: {msg_entry.get()}"
    msg_entry.delete(0, tk.END)
    client.send(message.encode('utf-8'))

send_btn = tk.Button(root, text="Send", command=send_message)
send_btn.pack(padx=20, pady=5)
root.bind('<Return>', send_message)

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                chat_area.config(state='normal')
                chat_area.insert(tk.END, message + "\n")
                chat_area.config(state='disabled')
                chat_area.yview(tk.END)
        except:
            print("An error occurred!")
            client.close()
            break

threading.Thread(target=receive_messages, daemon=True).start()
root.mainloop()
