"""
Tic Tac Toe Player
"""

import math

import copy
from os import truncate


class InvalidActionError(Exception):
    pass


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
    # raise NotImplementedError

    X_plays_count = 0
    O_plays_count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                X_plays_count += 1
            elif board[i][j] == O:
                O_plays_count += 1

    if O_plays_count < X_plays_count:
        return O
    else:
        return X               



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # raise NotImplementedError

    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i,j))

    return actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # raise NotImplementedError

    i = action[0]
    j = action[1]
    if board[i][j] != EMPTY:
        raise InvalidActionError

    play = player(board)
    result_board = copy.deepcopy(board)
    result_board[i][j] = play

    return result_board



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # raise NotImplementedError

    winner = None

    for i in range(3):
        if board[i][0] != EMPTY:
            winner = board[i][0]
            for j in range(1, 3):
                if board[i][j] != winner:
                    winner = None
                    break

        if winner is not None:
            return winner

    for j in range(3):
        if board[0][j] != EMPTY:
            winner = board[0][j]
            for i in range(1, 3):
                if board[i][j] != winner:
                    winner = None
                    break

        if winner is not None:
            return winner

    if board[0][0] != EMPTY:
        if board[1][1] == board[0][0] and board[2][2] == board[0][0]:
            return board[0][0]
        

    if board[0][2] != EMPTY:
        if board[1][1] == board[0][2] and board[2][0] == board[0][2]:
            return board[0][2]

    return winner



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # raise NotImplementedError

    win = winner(board)
    if win is not None:
        return True
    else:
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    return False
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # raise NotImplementedError

    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # raise NotImplementedError

    if terminal(board):
        return None

    action = None
    acts = actions(board)
    play = player(board)

    if play == X:
        value = -math.inf

        for act in acts:
            val = min_value(result(board,act))
            if val > value:
                value = val
                action = act

    elif play == O:
        value = math.inf

        for act in acts:
            val = max_value(result(board,act))
            if val < value:
                value = val
                action = act
        
    return action


def min_value(board):
    if terminal(board):
        return utility(board)

    value = math.inf
    acts = actions(board)

    for act in acts:
        value = min(value, max_value(result(board,act)))

    return value


def max_value(board):
    if terminal(board):
        return utility(board)

    value = -math.inf
    acts = actions(board)

    for act in acts:
        value = max(value, min_value(result(board,act)))

    return value
