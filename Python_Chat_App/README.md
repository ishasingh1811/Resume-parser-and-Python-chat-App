# 💬 Python Chat Application (LAN)

A simple real-time LAN chat app built using **Python**.  
It allows multiple users to chat over a local network with a clean **Tkinter GUI**, and automatically logs all messages.

---

## 🚀 Features
- Real-time chat between multiple clients  
- GUI built with Tkinter  
- Handles multiple users using threading  
- Stores chat messages in log files  
- Works offline over LAN (no internet needed)

---

## 🛠️ Tech Stack
- **Language:** Python 3  
- **Libraries:** socket, threading, tkinter, os, datetime  

---

## 📁 Folder Structure
Python-Chat-App/
│
├── server/
│ └── server.py
│
├── client/
│ └── client_gui.py
│
├── logs/
│ └── chat_logs.txt
│
└── README.md
---

## ⚙️ Installation & Setup
1. Clone this repository  
   ```bash
   git clone https://github.com/yourusername/python-chat-app.git
   cd python-chat-app
   Run the server
cd server
python server.py
Run the client GUI
cd client
python client_gui.py
Enter your name and start chatting 🎉
📚 How It Works
The server listens for new clients on a local port.
Each client connects and sends messages via sockets.
Messages are broadcast to all connected users in real time.
Every chat message is saved in logs/chat_logs.txt.
