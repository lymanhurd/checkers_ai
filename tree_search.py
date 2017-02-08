import logging

from evaluate import evaluate
from moves import find_children, has_jump, flip
from moves_test import STARTING_BOARD

__author__ = 'lhurd'

NEGATIVE_INFINITY = -99999
INFINITY = 99999
INITIAL_DEPTH = 8


def find_move(board, is_black):
    """Find the computer's move.

    Args:
      board: current board string
      is_black: True if current player is black

    Returns:
      The best move or None if the game has been lost.
    """
    # The UI uses the convention that unused spaces are '-'.
    board = board.replace('-', ' ')
    if not is_black:
        board = flip(board)
    best_child = None
    best_value = NEGATIVE_INFINITY
    children = sorted(find_children(board), key=evaluate, reverse=True)
    for child in children:
        value = negamax(child, INITIAL_DEPTH, NEGATIVE_INFINITY, INFINITY)
        if value > best_value:
            best_value = value
            best_child = child
    if best_child and not is_black:
        result = flip(best_child)
    else:
        result = best_child
    return result.replace(' ', '-')


def negamax(board, depth, alpha, beta):
    """Perform an alpha beta search of the move tree using the symmetry
    that we can flip the board to always look at things from black's point
    of view.

    Args:
      board: board string
      depth: depth of search (overridden if captures are possible)
      alpha: the alpha cut-off
      beta: the beta cut-off

    Returns:
      The evaluation value (integer) of the initial move represented by
      board.
    """

    # We do not stop the search if there are pending captures.
    if depth <= 0 and not has_jump(board):
        return evaluate(board)
    best_value = NEGATIVE_INFINITY
    children = find_children(board)
    for child in children:
        value = negamax(flip(child), depth - 1, -beta, -alpha)
        best_value = max(best_value, value)
        alpha = max(alpha, value)
        if alpha > beta:
            break
    return best_value


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    cumulative = 0
    for tests in range(500):
        bd = STARTING_BOARD
        black = True
        for i in range(50):
            # print 'Move %d' % i
            bd = find_move(bd, black)
            if bd:
                cumulative += evaluate(bd)
            else:
                print '%s wins.' % ('black' if black else 'red')
                break
            black = not black
            print bd
            # print_board(bd)
        print cumulative
