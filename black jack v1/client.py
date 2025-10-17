import socket
import threading
import json

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345


def d(data):
    return json.dumps(data).encode('utf-8')


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            try:
                message = json.loads(data.decode())
            except json.JSONDecodeError:
                print(data.decode())
            else:
                if "command" in message:
                    cmd = message.get("command")
                    if cmd == "name_request":
                        name = input("Choose your name: ")
                        sock.sendall(d({"command": "name_send", "data": name}))
                    elif cmd == "message":
                        print(message.get("data"))
                    else:
                        print(f"[DEBUG] Unknown message: {message}")
                else:
                    print(f"[DEBUG] {message}")
        except ConnectionResetError:
            print("Connection closed by server.")
            break


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print(f"Connected to server {SERVER_IP}:{SERVER_PORT}")

    try:
        receive_messages(client_socket)
    except KeyboardInterrupt:
        client_socket.close()
        print("Disconnected from server.")


if __name__ == "__main__":
    start_client()
