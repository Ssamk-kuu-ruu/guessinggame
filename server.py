import socket
import threading
import random

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
BANNER = """Enter your name: """

leaderboard = []

def choose_difficulty(diff):
    if diff == '1':
        return random.randint(1, 50)
    
    elif diff == '2':
        return random.randint(1, 100)
    
    elif diff == '3':
        return random.randint(1, 500)
    
def handle_client(client, addr):
    try:
        client.sendall(BANNER.encode())
        player = client.recv(1024).decode().strip()
        print(f"[CONNECTED]     {player} connected...")
        client.sendall(b"Choose difficulty level:\n(1) Easy (1 - 50)\n(2) Medium (1 - 100)\n(3) Hard (1 - 500)\n")
        diff = client.recv(1024).decode().strip().lower()

        while True:
            guessme = choose_difficulty(diff)
            client.sendall(b"Enter your guess:\n")
            tries = 0
            lives = 10

            while True:
                try:
                    client_input = client.recv(1024)
                    if not client_input:
                        print(f"[DISCONNECTED]     Player {player} disconnected.")
                        return
                    
                    guess = int(client_input.decode().strip())
                    tries += 1
                    lives -= 1

                    if guess == guessme:
                        score = (lives * 100) + 50
                        client.sendall(f"Correct Answer!\nYour score: {score}\n".encode())
                        leaderboard.append({'name': player, 'score': score, 'difficulty': diff})
                        print(f"[CONGRATULATIONS]     Player {player} guessed the number {guessme} in {tries} tries!")
                        break

                    elif guess > guessme:
                        client.sendall(b"Guess Lower!\n")

                    elif guess < guessme:
                        client.sendall(b"Guess Higher!\n")

                except ConnectionResetError:
                    print(f"[DISCONNECTED]     Connection with player {player} forcibly closed by the remote host.")
                    return 

    except ConnectionAbortedError:
        print(f"[DISCONNECTED]     Connection with player {player} aborted.")

    finally:
        conn.close()

def get_score(player):
    return player['score']

def display_leaderboard():
    global leaderboard
    print("\n== Leaderboard ==\n")
    for i, player in enumerate(sorted(leaderboard, key=get_score, reverse=True)):
        print(f"Rank {i+1}:")
        print(f"Name: {player['name']}")
        print(f"Score: {player['score']}")
        print(f"Difficulty: {player['difficulty']}\n")



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen(5)

print(f"[WAITING]     Server is listening on port {PORT}")

while True:
    conn, addr = server.accept()
    print(f"[NEW CONNECTION]     New connection from {SERVER}({PORT})")
    clients = threading.Thread(target=handle_client, args=(conn, addr))
    clients.start()
    print(f"[ACTIVE CONNECTIONS]     {threading.active_count() - 1}")
    clients.join()
    display_leaderboard()

