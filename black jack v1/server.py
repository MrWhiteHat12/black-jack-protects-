# server.py
import socket
import threading
import json
import multiplayer

player_setup = False
HOST = '127.0.0.1'   
PORT = 12345         # port to bind on

connected_players = []   # list of PlayerConnection objects (by name)
numbered_players = []    # list of PlayerConnection objects (by number)
number_joined = 1


def d(data):
    return json.dumps(data).encode('utf-8')  


class PlayerConnection:
    def __init__(self, connection, id, num):
        self.connection = connection
        self.id = id
        self.name = 'Unknown'
        self.num = num  
        self.connection.sendall(d({"command": "name_request"}))

    def handle(self, data):
        if data.get('command') == 'name_send':
            self.name = data.get('data')
            print(f"[+] Player connected: {self.name} (#{self.num})")
        elif data.get('command') == 'message':
            print(f"{self.name}: {data.get('data')}")


def broadcast(message):
    for connection_object in connected_players:
        try:
            connection_object.connection.send(message)
        except:
            connection_object.connection.close()
            if connection_object in connected_players:
                connected_players.remove(connection_object)


def targeted_message_name(message, target_name):
    for player in connected_players:
        if player.name == target_name:
            try:
                player.connection.send(
                    d({"command": "message", "data": message}))
                print(f"Sent message to {player.name}: {message}")
            except:
                player.connection.close()
                connected_players.remove(player)
            break
    else:
        print(f"Player '{target_name}' not found.")


def targeted_message_num(message, target_num):
    for player in numbered_players:
        if str(player.num) == str(target_num):  # make sure it works even if user types string
            try:
                player.connection.send(
                    d({"command": "message", "data": message}))
                print(f"Sent message to player #{player.num}: {message}")
            except:
                player.connection.close()
                numbered_players.remove(player)
            break
    else:
        print(f"Player number {target_num} not found.")


def handle_client(client_socket, addr):
    global number_joined
    print(f"[+] New connection from {addr}")
    connection_object = PlayerConnection(
        connection=client_socket, id=len(connected_players), num=number_joined
    )
    connected_players.append(connection_object)
    numbered_players.append(connection_object)
    number_joined += 1

    try:
        while True:
            data = connection_object.connection.recv(1024)
            if not data:
                break
            connection_object.handle(json.loads(data.decode()))
    except ConnectionResetError:
        print(f"[!] Connection lost: {addr}")
    finally:
        print(f"[-] Client {addr} disconnected")
        if connection_object in connected_players:
            connected_players.remove(connection_object)
        if connection_object in numbered_players:
            numbered_players.remove(connection_object)
        connection_object.connection.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[✓] Server listening on {HOST}:{PORT}")

    # Thread for server input (optional)
    threading.Thread(target=server_input, daemon=True).start()

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()


def server_input():
    while True:
        msg = input()
        if msg.startswith("@"):  # message to specific player by NAME
            parts = msg.split(" ", 2)
            if len(parts) >= 3:
                target_name = parts[1]
                message = parts[2]
                targeted_message_name(message, target_name)
            else:
                print("Usage: @ name message")

        elif msg.startswith("/"):  # message to specific player by NUMBER
            parts = msg.split(" ", 2)
            if len(parts) >= 3:
                target_num = parts[1]
                message = parts[2]
                targeted_message_num(message, target_num)
            else:
                print("Usage: / number message")

        else:
            # broadcast message to everyone
            broadcast(d({"command": "message", "data": msg}))


if __name__ == "__main__":
    start_server()
