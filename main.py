import game
from camera import procitaj
import subprocess
import serial.tools.list_ports

print("Welcome to Tic Tac Toe")
print("Please select a port for the robot:")
ports = serial.tools.list_ports.comports()
index = 1
for port in ports:
    print(f'{index}. {port}')
    index += 1

index -= 1

num = int(input(f'Please enter a number between 1 and {index}: ')) - 1
selected_port = ports[num]
winner = None
while True:
    checkinput = input("Is the field already drawn? Yes/No")
    if checkinput.lower() == 'no':
        subprocess.Popen(["python", "draw.py", str(f'{selected_port}').split(" ")[0], "field"])
        break
    elif checkinput.lower() == 'yes':
        break
    else:
        print("Please answer with yes or no.")

player = ''
while True:
    player = input('Choose your side: X or O ')

    if player.lower() == 'x' or player.lower() == 'o':
        break
    else:
        print('Type X/O')

if player.lower() == 'x':
    while winner is None:
        input("Press Enter to when you have done your move...")
        game.board = procitaj()
        winner = game.check_winner(game.board)
        if winner is not None:
            break
        best_move = game.find_best_move(game.board, 'o')
        print(best_move)
        print("drawing at:", f'{(2 - best_move[1]) + best_move[0] * 3 + 1}')
        subprocess.Popen(["python", "draw.py", str(f'{selected_port}').split(" ")[0], "o",
                          f'{best_move[1] + (2 - best_move[0]) * 3 + 1}']).wait()
        game.make_move(game.board, "o", best_move)
        game.print_board(game.board)
        winner = game.check_winner(game.board)
        if winner is not None:
            break
        print("Your turn...")
else:
    while winner is None:
        game.board = procitaj()
        winner = game.check_winner(game.board)
        if winner is not None:
            break
        best_move = game.find_best_move(game.board, 'x')
        print(best_move)
        print("drawing at:", f'{(2 - best_move[1]) + best_move[0] * 3 + 1}')
        subprocess.Popen(["python", "draw.py", str(f'{selected_port}').split(" ")[0], "x",
                          f'{best_move[1] + (2 - best_move[0]) * 3 + 1}']).wait()
        game.make_move(game.board, "x", best_move)
        game.print_board(game.board)
        winner = game.check_winner(game.board)
        if winner is not None:
            break
        print("Your turn...")
        input("Press Enter to when you have done your move...")

if winner.upper() == 'DRAW':
    print("It's a draw...")
else:
    print(winner.upper(), 'won. Congratulations!')
