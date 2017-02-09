"""Evaluate the strength of a position specified as a 32-long string of
b, B, r, R (capitals are kings).  We limit the discussion to evaluation
functions with the property that:
evaluation(board) = - evaluation(flip(board))
where the flip operation consists of reversing the string and substituting
r <--> b and R <--> B.  We make the assumption that positive scores are
better for black.
"""

__author__ = 'lhurd'

# Almost the simplest possible evaluation function.  We use the heuristic
# that a king is worth 3/2 of a normal checker, a ratio cited in the book
# Blondie24 (alongside the explanation that they were not using this
# heuristic),  I expect the rest of the code to stabilize and eventually
# the main goal of his project will be making this function smarter.  For
# example, in this simple form the program cannot decide between sequences
# that do not have a capture.


# The calling code is supposed to have accounted for the cases where the
# move is a  win for one player or a draw.
def evaluate(board):
    """Evaluate a checkers board via a simple linear heuristic.

    Args:
        board: a string representing a board.

    Returns:
        an integer which is positive if black has te upper hand (negative
        for red).
    """
    return (30 * board.count('B') + 20 * board.count('b') - 30
            * board.count('R') - 20 * board.count('r'))
