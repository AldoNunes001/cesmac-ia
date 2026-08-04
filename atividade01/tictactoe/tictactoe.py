"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    count_o_moves = 0
    count_x_moves = 0

    for row in board:
        for cell in row:
            if cell == X:
                count_x_moves += 1
            elif cell == O:
                count_o_moves += 1

    if count_x_moves > count_o_moves:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for index, row in enumerate(board):
        for index2, cell in enumerate(row):
            if cell == EMPTY:
                actions.add((index, index2))

    return actions


def copy(board):
    return [row[:] for row in board]

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy(board)
    index, index2 = action
    if new_board[index][index2] != EMPTY:
        raise ValueError("Movimento inválido")
    new_board[index][index2] = player(board)
        
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    for row in board:
        if row[0] == row[1] == row[2]:
            return row[0]

    for column in range(3):
        if board[0][column] == board[1][column] == board[2][column] != EMPTY:
            return board[0][column]

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    if len(actions(board)) == 0:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)

    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    return 0

def max_value(board):
    if terminal(board):
        return utility(board)

    value = -math.inf

    for action in sorted(actions(board)):
        value = max(value, min_value(result(board, action)))

    return value


def min_value(board):
    if terminal(board):
        return utility(board)

    value = math.inf

    for action in sorted(actions(board)):
        value = min(value, max_value(result(board, action)))

    return value

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    if player(board) == X:
        best_value = -math.inf
        best_action = None

        for action in sorted(actions(board)):
            value = min_value(result(board, action))

            if value > best_value:
                best_value = value
                best_action = action

        return best_action

    else:
        best_value = math.inf
        best_action = None

        for action in sorted(actions(board)):
            value = max_value(result(board, action))

            if value < best_value:
                best_value = value
                best_action = action

        return best_action