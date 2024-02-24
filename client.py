# import required modules
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import el_gamal

HOST = '127.0.0.1'
PORT = 1234

DARK_GREY = '#89CFF0'  
MEDIUM_GREY = '#FFB6C1' 
OCEAN_BLUE = '#e75480'  
WHITE = "black"  
FONT = ("Times Roman", 15)  
BUTTON_FONT = ("Times Roman", 15) 
SMALL_FONT = ("Times Roman", 13)  

# Creating a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# List to store usernames
used_usernames = []

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    # Get the username entered by the user
    username = username_textbox.get().strip()

    # Check if the username is already in use
    if username in used_usernames:
        messagebox.showerror("Username already in use",
                    "This username is already in use. Please choose another one.")
        return
    
    # Add the username to the list of used usernames
    used_usernames.append(username)

    # Your existing code for connecting to the server and setting up the UI
    try:
        # Connect to the server
        client.connect(('127.0.0.1', 1234))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", 
                    f"Unable to connect to server {HOST} {PORT}")

    # Send the username to the server
    if username != '':
        client.sendall(username.encode())
        print("SEND : ", username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()


    # Update the UI
    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)
    username_button.pack_forget()
    username_textbox.pack_forget()
    username_label['text'] = "Welcome " + username + " to our secure room"
    username_label.pack(side=tk.LEFT)

def send_message():
    message = message_textbox.get()
    if message != '':
        message_textbox.delete(0, len(message))
        
        if flagMethod == 1:
            print("elgammel encryption")
            global messageCopy
            message = el_gamal.incrypt_gamal(int(elgamalkey[0]), int(elgamalkey[1]), 
                                    int(elgamalkey[2]),message)

            print("message text= ",message)
            #{q, a, YA, XA}

            messageCopy = message
        
        client.sendall(message.encode("utf-8"))
        print("SEND : ", message.encode() )
        
        print("This message has been delivered")
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        print("RECV : ", message)
        
        if message != '':
            message = message.split("~")
            global key, flagMethod, elgamalkey, rsa_string

            username = message[0]
            content = message[1]
            key = message[2]
            flagMethod = int(message[3])
            elgamalkey = message[4]
            elgamalkey = elgamalkey.split(",")
            rsa_string = message[5]
            rsa_string = rsa_string.split(",")

            if username != "SERVER":                
                if flagMethod == 1:
                    print("elgamal decryption")
                    print("content copy message=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==- ", content)
                    content = el_gamal.decrept_gamal(content, int(elgamalkey[3]))

            add_message(f"[{username}] {content}")
        else:
            messagebox.showerror("Error", "Message recevied from client is empty")

root = tk.Tk()
root.geometry("600x600")
root.title("Messenger Client")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)


username_label = tk.Label(top_frame, text="Enter your username :", 
                          font=FONT,Sbg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, 
                            bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, 
                            bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, 
                           bg=MEDIUM_GREY, fg=WHITE, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, 
                           bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT,
                                         bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

# main function
def main():
    root.mainloop()

if __name__ == '__main__':
    main()
