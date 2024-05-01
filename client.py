import socket

PORT = 5050
SERVER = "192.168.189.37"
ADDR = (SERVER, PORT)

def play_game():
    server = socket.socket()
    server.connect(ADDR)

    data = server.recv(1024)
    print("""\n=== Enhanced Guessing Game v2.0 ===\n""")

    print(data.decode().strip())

    while True:

        user_input = input("> ").strip()
        server.sendall(user_input.encode())

        print("***********************")

        recieve = server.recv(1024).decode().strip()

        if "Correct" in recieve:
            print(recieve)
            break

        print(recieve)
        continue

    server.close()

while True:
    play_game()
    repeat = input("\nDo you want to play again? (y / n): ").strip().lower()
    if repeat == "n":
        break