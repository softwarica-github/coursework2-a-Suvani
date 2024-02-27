import threading
import time
import server

# Function to simulate setting up integration testing
def setUpClass():
    print("Setting up Unit testing...")
    server_thread = threading.Thread(target=server)
    server_thread.start()
    time.sleep(1)
    return server_thread

# Function to simulate tearing down integration testing
def tearDownClass(server_thread):
    print("Tearing down unit testing...")
    server_thread.join()
    print("Integration testing done.")

# Function to simulate testing client-server communication
def test_client_server_communication():
    print("Testing client-server communication...")
    time.sleep(2)

    username = "TestUser"
    print(f"Sending username to server: {username}")
    time.sleep(1)

    message = "Hello, world!"
    print(f"Sending message to server: {message}")
    time.sleep(1)

if __name__ == '__main__':
    server_thread = setUpClass()
    test_client_server_communication()
    tearDownClass(server_thread)
