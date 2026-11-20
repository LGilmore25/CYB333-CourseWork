import socket

# Server configuration
HOST = '127.0.0.1'
PORT = 45678

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow the server to reuse the address after restarting
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen()

    print(f"Server is listening on {HOST}:{PORT}")
    print("Waiting for a client to connect...")

    # Accept an incoming client connection
    client_socket, client_address = server_socket.accept()

    print(f"Connection established with {client_address}")

    # Receive messages from the client
    data = client_socket.recv(1024)

    if data:
        message = data.decode('utf-8')
        print(f"Client says: {message}")

        # Send a response back to the client
        response = "Message received by server!"
        client_socket.sendall(response.encode('utf-8'))

        print("Response sent to client.")
    else:
        print("Client disconnected without sending a message.")

except KeyboardInterrupt:
    print("\nServer interrupted by user.")

except OSError as error:
    print(f"Server error: {error}")

finally:
    # Close the client connection if one was established
    if 'client_socket' in locals():
        client_socket.close()
        print("Client connection closed.")
    # Close the server socket
    server_socket.close()
    print("Server socket closed.")
