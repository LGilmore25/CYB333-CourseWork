import socket

# Server configuration
HOST = '127.0.0.1'
PORT = 45678

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((HOST, PORT))

    print(f"Connected to server at {HOST}:{PORT}")

    # Send a message to the server
    message = "Hello from the client!"
    client_socket.sendall(message.encode('utf-8'))

    print("Message sent to server.")

    # Receive the server's response
    data = client_socket.recv(1024)

    if data:
        response = data.decode('utf-8')
        print(f"Server response: {response}")
    else:
        print("Server closed the connection without sending a response.")

except ConnectionRefusedError:
    print("Connection failed. Make sure the server is running.")

except OSError as error:
    print(f"Client error: {error}")

finally:
    # Close the client socket
    client_socket.close()
    print("Client socket closed.")
