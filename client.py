import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import key2

HOST = '127.0.0.1'
PORT = 1234

WARM_VIOLET = '#4169E1'
ORANGE = '#9370DB'
DARK_BROWN = '#654321'
BLACK = "black"
FONT = ("Times New Roman", 17)
BUTTON_FONT = ("Times New Roman", 15)
SMALL_FONT = ("Times New Roman", 13)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
        print("SEND : ", username.encode() )
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)
    username_button.pack_forget()
    username_textbox.pack_forget()
    username_label['text'] = "user " + username + " is ONLINE ✅ "
    username_label.pack(side=tk.LEFT)

def send_message():
    message = message_textbox.get()
    if message != '':
        message_textbox.delete(0, len(message))
        
        # Encryption based on flagMethod
        if flagMethod == 1:  # ElGamal encryption
            message = key2.incrypt_gamal(int(elgamalkey[0]), int(elgamalkey[1]), int(elgamalkey[2]), message)
        
        client.sendall(message.encode("utf-8"))
        print("SEND : ", message.encode() )
        print("This message has been delivered")
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

def listen_for_messages_from_server(client):
    while True:
        message = client.recv(2048).decode('utf-8')
        print("RECV : ", message)
        if message != '':
            message = message.split("~")
            global key, flagMethod, elgamalkey

            username = message[0]
            content = message[1]
            key = message[2]
            flagMethod = int(message[3])
            elgamalkey = message[4]
            elgamalkey = elgamalkey.split(",")

            if username != "SERVER":
                if flagMethod == 1:  # ElGamal decryption
                    content = key2.decrept_gamal(content, int(elgamalkey[3]))

            add_message(f"[{username}] {content}")
        else:
            messagebox.showerror("Error", "Message received from client is empty")

root = tk.Tk()
root.geometry("600x600")
root.title("CHAT APP")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=WARM_VIOLET)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=WARM_VIOLET)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=WARM_VIOLET)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="USERNAME:", font=FONT, bg=WARM_VIOLET, fg=BLACK)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=ORANGE, fg=BLACK, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="CONNECT", font=BUTTON_FONT, bg=DARK_BROWN, fg=BLACK, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=ORANGE, fg=BLACK, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=DARK_BROWN, fg=BLACK, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=ORANGE, fg=BLACK, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

def main():
    root.mainloop()

if __name__ == '__main__':
    main()
