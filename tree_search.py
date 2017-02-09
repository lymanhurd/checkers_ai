import random
import logging

from evaluate import evaluate
from moves import find_children, has_jump, flip
from moves_test import STARTING_BOARD

__author__ = 'lhurd'

NEGATIVE_INFINITY = -99999
INFINITY = 99999
INITIAL_DEPTH = 3


def find_move(board, is_black):
    """Find the computer's move.

    Args:
      board: current board string
      is_black: True if current player is black

    Returns:
      The best move or None if the game has been lost.
    """
    # The UI uses the convention that unused spaces are '-'.
    if not is_black:
        board = flip(board)
    best_child = None
    best_children = []
    best_value = NEGATIVE_INFINITY
    for child in find_children(board):
        value = negamax(child, INITIAL_DEPTH, NEGATIVE_INFINITY, INFINITY)
        if value > best_value:
            best_value = value
            best_children = []
        if value >= best_value:
            best_children.append(child)
    # If there are ties, choose randomly from among the tied choices.
    if best_children:
        best_child = best_children[random.randint(0, len(best_children) - 1)]
    if best_child and not is_black:
        result = flip(best_child)
    else:
        result = best_child
    logging.debug('final eval %d bd %s' % (best_value, result))
    return result


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
        value = evaluate(board)
        if depth % 2:
            logging.debug('leaf depth %d eval %d bd %s' % (depth, -value,
                                                           flip(board)))
        else:
            logging.debug(
                'leaf depth %d eval %d bd %s' % (depth, value, board))
        return value
    best_value = NEGATIVE_INFINITY
    children = sorted(find_children(board), key=evaluate, reverse=True)
    for child in children:
        value = - negamax(flip(child), depth - 1, -beta, -alpha)
        logging.debug('node depth %d eval %d' % (depth, (-1) ** depth * value))
        best_value = max(best_value, value)
        alpha = max(alpha, value)
        if alpha > beta:
            break
    return best_value


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bd = STARTING_BOARD
    black = True
    i = 0
    while bd:
        bd = find_move(bd, black)
        if not bd:
            print '%s wins.' % ('red' if black else 'black')
            break
        black = not black
        i += 1
        print '%3d %s' % (i, bd)
