import unittest
import threading
import time
import sys
sys.path.append(".")  # Add the current directory to the system path
from server import server  # Importing the server module and specifically the 'server' function or attribute

class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_thread = threading.Thread(target=server)
        cls.server_thread.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        server.running = False
        cls.server_thread.join()
        print("Integration testing done.")

    def test_client_server_communication(self):
        print("Simulating client-server communication...")
        time.sleep(2)

        username = "TestUser"
        print(f"Client sent username: {username}")
        time.sleep(1)

        message = "Hello, world!"
        print(f"Client sent message: {message}")
        time.sleep(1)

if __name__ == '__main__':
    unittest.main()
