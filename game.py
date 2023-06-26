import math

def print_board(board):
    print("---------")
    for i in range(3):
        row = "| "
        for j in range(3):
            if board[i][j] == "_":
                row += "_ | "
            else:
                row += board[i][j].lower() + " | "
        print(row)
        print("---------")

def make_move(board, player, move):
    if board[move[0]][move[1]] == "_":
        board[move[0]][move[1]] = player
        return True
    else:
        return False

def check_winner(board):
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "_":
            return board[i][0]

    # Check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != "_":
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != "_":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "_":
        return board[0][2]

    # Check for a draw
    is_draw = True
    for i in range(3):
        for j in range(3):
            if board[i][j] == "_":
                is_draw = False
                break
    if is_draw:
        return "draw"

    # No winner yet
    return None

def evaluate(board):
    # Evaluate the board state
    winner = check_winner(board)
    if winner == "x":
        return 1
    elif winner == "o":
        return -1
    else:
        return 0

def minimax(board, depth, maximizing_player, alpha, beta):
    if check_winner(board) is not None or depth == 0:
        return evaluate(board)

    if maximizing_player:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == "_":
                    board[i][j] = "x"
                    eval = minimax(board, depth - 1, False, alpha, beta)
                    board[i][j] = "_"
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == "_":
                    board[i][j] = "o"
                    eval = minimax(board, depth - 1, True, alpha, beta)
                    board[i][j] = "_"
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def find_best_move(board, player):
    best_eval = -math.inf
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == "_":
                board[i][j] = player
                eval = minimax(board, 9, False, -math.inf, math.inf)
                board[i][j] = "_"
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)
    return best_move

# Set up the initial board state
board = [["_", "_", "_"],
         ["_", "_", "_"],
         ["_", "_", "_"]]
