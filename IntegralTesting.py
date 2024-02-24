import unittest
import threading
import time
import socket
import client
import server

class TestIntegration(unittest.TestCase):
    def setUp(self):
        # # Start the server in a separate thread
        self.server_thread = threading.Thread(target=server.main)
        self.server_thread.start()
        time.sleep(1)  # Give some time for the server to start
        
        # Connect the client
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 1234))
        time.sleep(1)  # Give some time for the client to connect

    def tearDown(self):
        # Close the client socket
        self.client_socket.close()
        
        # Stop the server thread
        server.running = False
        self.server_thread.join()

    def test_client_server_communication(self):
        # Test client-server communication
        username = "TestUser"
        message = "Hello, world!"
        
        # Send username from client to server
        self.client_socket.sendall(username.encode())
        time.sleep(1)  # Give some time for the server to process
        
        # Send message from client to server
        self.client_socket.sendall(message.encode())
        time.sleep(1)  # Give some time for the server to process

if __name__ == '__main__':
    unittest.main()
