import random


def instruction():
    print("Welcome in tic-tac-toe game, where you can choose difficulty level"
          "\nHere is a game-table")
    print('''
 0 | 1 | 2
 ---------
 3 | 4 | 5
 ---------
 6 | 7 | 8 ''')


def show_board(table):
    # display current board
    print("\n\t", table[0], "|", table[1], "|", table[2])
    print("\t", "---------")
    print("\t", table[3], "|", table[4], "|", table[5])
    print("\t", "---------")
    print("\t", table[6], "|", table[7], "|", table[8], "\n")


def whos_turn():
    # decides who starts
    decision = int(input("Who should start?"
                         "\n1-Me"
                         "\n2-Computer\n"))
    if decision == 1:
        user = X
        comp = O
        return user, comp
    elif decision == 2:
        user = O
        comp = X
        return user, comp


def win_condition(table):
    # win conditions
    win_list = ((0, 1, 2),
                (3, 4, 5),
                (6, 7, 8),
                (0, 3, 6),
                (1, 4, 7),
                (2, 5, 8),
                (0, 4, 8),
                (2, 4, 6))

    for row in win_list:
        if table[row[0]] == table[row[1]] == table[row[2]] != empty:
            win = table[row[0]]
            return win

    if empty not in table:
        return "REMIS"


def next_turn(next):
    # change of turn
    if next == X:
        next = O
    else:
        next = X
    return next


def win_information(winner, computer, human):
    # Shows who win
    if winner == player:
        print("YOU WIN!!!")
    elif winner == computer:
        print("YOU LOSE!!!")
    elif winner == "REMIS":
        print("REMIS!!!")


def empty_position(table):
    # Creates list of available sections
    emptyList = []
    for i in range(9):
        if table[i] == empty:
            emptyList.append(i)
    return emptyList


def human_move(board):
    # Allows player make a move only on free places
    free_space = empty_position(board)
    position = None
    while position not in free_space:
        position = int(input("Choose place\n"))
        if position not in free_space:
            print("Place taken, choose another")
    return position


def computer_move(board):
    # Computer moves depends of the difficulty level
    if level == 1:
        # Computer plays random
        position = None
        while position not in empty_position(board):
            position = random.randrange(0, 9)
            if position not in empty_position(board):
                position = random.randrange(0, 9)
        return position

    if level == 2:
        # Computer plays random and seeks to win
        for position in empty_position(board):
            # Checks if can win
            board[position] = computer
            if win_condition(board) == computer:
                return position
            board[position] = empty

        for position in empty_position(board):
            position = random.randrange(0, 9)
            if position not in empty_position(board):
                position = random.randrange(0, 9)
            return position

    if level == 3:
        # Computer plays random and seeks to win, blocks opponent
        for position in empty_position(board):
            # Checks if can win
            board[position] = computer
            if win_condition(board) == computer:
                return position
            board[position] = empty

        for position in empty_position(board):
            # Checks if the opponent can win, and blocks him
            board[position] = player
            if win_condition(board) == player:
                return position
            board[position] = empty

        for position in empty_position(board):
            position = random.randrange(0, 9)
            if position not in empty_position(board):
                position = random.randrange(0, 9)
            return position

    if level == 4:
        # Computer plays random and seeks to win, blocks opponent, have defined best moves
        best_moves = (4, 0, 2, 6, 8, 1, 3, 5, 7)
        for position in empty_position(board):
            board[position] = computer
            if win_condition(board) == computer:
                return position
            board[position] = empty

        for position in empty_position(board):
            board[position] = player
            if win_condition(board) == player:
                return position
            board[position] = empty

        for position in best_moves:
            # Computer plays according to the best moves
            if position in empty_position(board):
                return position

    if level == 5:
        # Computer plays random and seeks to win, blocks opponent, have defined best moves which choose randomly
        best_move = 4
        best_moves_corner = (0, 2, 6, 8)
        best_move_rest = (1, 3, 5, 7)

        for position in empty_position(board):
            board[position] = computer
            if win_condition(board) == computer:
                return position
            board[position] = empty

        for position in empty_position(board):
            board[position] = player
            if win_condition(board) == player:
                return position
            board[position] = empty

        if best_move in empty_position(board):
            # Checks if the center is empty
            return best_move

        for position in empty_position(board):
            # Plays randomly on corners
            position = random.choice(best_moves_corner)
            if position not in empty_position(board):
                position = random.choice(best_moves_corner)
            return position

        for position in empty_position(board):
            position = random.choice(best_move_rest)
            if position not in empty_position(board):
                position = random.choice(best_move_rest)
            return position

    if level == 6:
        # Computer plays randomly seeks to win and always blocks opponent
        best_move = 4
        best_moves_corner = (0, 2, 6, 8)
        best_move_rest = (1, 3, 5, 7)

        for position in empty_position(board):
            board[position] = computer
            if win_condition(board) == computer:
                return position
            board[position] = empty

        for position in empty_position(board):
            board[position] = player
            if win_condition(board) == player:
                return position
            board[position] = empty

        if board[4] == computer and board[0] == player:
            position = 8
            if board[position] == empty:
                return position

        if board[4] == computer and board[2] == player:
            position = 6
            if board[position] == empty:
                return position

        if board[4] == computer and board[6] == player:
            position = 2
            if board[position] == empty:
                return position

        if board[4] == computer and board[8] == player:
            position = 0
            if board[position] == empty:
                return position

        if best_move in empty_position(board):
            return best_move

        for position in empty_position(board):
            position = random.choice(best_moves_corner)
            if position not in empty_position(board):
                position = random.choice(best_moves_corner)
            return position

        for position in empty_position(board):
            position = random.choice(best_move_rest)
            if position not in empty_position(board):
                position = random.choice(best_move_rest)
            return positio


empty = " "
board = []
X = 'X'
O = 'O'

for i in range(0, 9):
    board.append(empty)

turn = X
instruction()
level = int(input(
    "Choose level of difficulty:"
    "\n1-Very easy"
    "\n2-Easy"
    "\n3-Normal"
    "\n4-Very hard"
    "\n5-Nightmare"
    "\n6-Impossible to win"))

player, computer = whos_turn()

while not win_condition(board):
    if turn == player:
        board[human_move(board)] = player
    if turn == computer:
        board[computer_move(board)] = computer
    turn = next_turn(turn)
    show_board(board)
    winner = win_condition(board)
    win_information(winner, computer, player)
