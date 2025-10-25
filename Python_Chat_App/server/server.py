import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 55555

# Ensure logs folder exists
# if not os.path.exists("../logs"):
#     os.makedirs("../logs")

# LOG_FILE = "../logs/chat_logs.txt"

# Create logs folder in base directory safely
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "chat_logs.txt")

def save_to_log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message, client=None):
    # Send to all clients except sender
    for c in clients:
        if c != client:
            try:
                c.send(message)
            except:
                c.close()
                clients.remove(c)
    # Save message to log file
    try:
        decoded = message.decode("utf-8")
        save_to_log(decoded)
    except:
        pass

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            nickname = nicknames[index]
            clients.remove(client)
            nicknames.remove(nickname)
            leave_msg = f"{nickname} left the chat!"
            broadcast(leave_msg.encode('utf-8'))
            client.close()
            break

def receive():
    print(f"[SERVER STARTED] on {HOST}:{PORT}")
    save_to_log("=== Server started ===")

    while True:
        client, address = server.accept()
        print(f"[NEW CONNECTION] {str(address)}")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of client is {nickname}")
        join_msg = f"{nickname} joined the chat!"
        broadcast(join_msg.encode('utf-8'))
        client.send("Connected to the server!".encode('utf-8'))
        save_to_log(join_msg)

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
