"""This module takes a checkers position as a 32 character string comprising "b", "B", "r", "R" and " " (capitals
represent kings) and returns a list of possible successor positions.  By use of the flip command (reversing the string
and replacing b <--> r and B <--> R, we can compute the moves solely from black's point of view and then invert if
necessary.

The rules of checkers state that if a capture is possible, no other type of move is legal.
"""
__author__ = 'lhurd'

import string

TABLE = string.maketrans('bBrR', 'rRbB')

FWD_MOVES = ((0, 4), (0, 5), (1, 5), (1, 6), (2, 6), (2, 7), (3, 7), (4, 8), (5, 8), (5, 9), (6, 9), (6, 10), (7, 10),
             (7, 11), (8, 12), (8, 13), (9, 13), (9, 14), (10, 14), (10, 15), (11, 15), (12, 16), (13, 16), (13, 17),
             (14, 17), (14, 18), (15, 18), (15, 19), (16, 20), (16, 21), (17, 21), (17, 22), (18, 22), (18, 23),
             (19, 23), (20, 24), (21, 24), (21, 25), (22, 25), (22, 26), (23, 26), (23, 27), (24, 28), (24, 29),
             (25, 29), (25, 30), (26, 30), (26, 31), (27, 31))

BWD_MOVES = ((4, 0), (5, 0), (5, 1), (6, 1), (6, 2), (7, 2), (7, 3), (8, 4), (8, 5), (9, 5), (9, 6), (10, 6), (10, 7),
             (11, 7), (12, 8), (13, 8), (13, 9), (14, 9), (14, 10), (15, 10), (15, 11), (16, 12), (16, 13), (17, 13),
             (17, 14), (18, 14), (18, 15), (19, 15), (20, 16), (21, 16), (21, 17), (22, 17), (22, 18), (23, 18),
             (23, 19), (24, 20), (24, 21), (25, 21), (25, 22), (26, 22), (26, 23), (27, 23), (28, 24), (29, 24),
             (29, 25), (30, 25), (30, 26), (31, 26), (31, 27))

FWD_JUMPS = ((0, 5, 9), (1, 5, 8), (1, 6, 10), (2, 6, 9), (2, 7, 11), (3, 7, 10), (4, 8, 13), (5, 8, 12), (5, 9, 14),
             (6, 9, 13), (6, 10, 15), (7, 10, 14), (8, 13, 17), (9, 13, 16), (9, 14, 18), (10, 14, 17), (10, 15, 19),
             (11, 15, 18), (12, 16, 21), (13, 16, 20), (13, 17, 22), (14, 17, 21), (14, 18, 23), (15, 18, 22),
             (16, 21, 25), (17, 21, 24), (17, 22, 26), (18, 22, 25), (18, 23, 27), (19, 23, 26), (20, 24, 29),
             (21, 24, 28), (21, 25, 30), (22, 25, 29), (22, 26, 31), (23, 26, 30))

BWD_JUMPS = ((8, 5, 1), (9, 5, 0), (9, 6, 2), (10, 6, 1), (10, 7, 3), (11, 7, 2), (12, 8, 5), (13, 8, 4), (13, 9, 6),
             (14, 9, 5), (14, 10, 7), (15, 10, 6), (16, 13, 9), (17, 13, 8), (17, 14, 10), (18, 14, 9), (18, 15, 11),
             (19, 15, 10), (20, 16, 13), (21, 16, 12), (21, 17, 14), (22, 17, 13), (22, 18, 15), (23, 18, 14),
             (24, 21, 17), (25, 21, 16), (25, 22, 18), (26, 22, 17), (26, 23, 19), (27, 23, 18), (28, 24, 21),
             (29, 24, 20), (29, 25, 22), (30, 25, 21), (30, 26, 23), (31, 26, 22))


def children(board, player_is_black):
    if not player_is_black:
        board = _flip(board)
    boards = [_apply_jump(board, m) for m in _jump_moves(board)]
    if not boards:
        boards = [_apply_move(board, m) for m in _normal_moves(board)]
    if player_is_black:
        return boards
    else:
        return [_flip(b) for b in boards]


def _flip(board):
    """Flip player whose turn it is so we can always look at things from black's point of view.

    Args:
      board: string containing initial board.

    Returns:
     flipped board.
    """
    return board.translate(TABLE)[::-1]  # NOTE: In all that follows, black is the current player.


#
# Logic for non-jump moves, i.e., a single forward diagonal move for any piece or a backward diagonal move for a king,
#
def _normal_moves(board):
    """Takes in a board string and return a set of tuples representing legal (non-jump) moves.

    Args:
      board: board string

    Returns:
      list of tuples giving start and finish coordinates
    """
    fwd = [t for t in FWD_MOVES if board[t[0]].lower() == 'b' and board[t[1]] == ' ']
    bwd = [t for t in BWD_MOVES if board[t[0]] == 'B' and board[t[1]] == ' ']
    return fwd + bwd


def _apply_move(board, move):
    """Apply a non-jump move to a given board.

    Args:
      board: board string
      move: move tuple

    Returns:
      Board string of new position.
    """
    assert (board[move[0]].lower() == 'b')
    board_list = list(board)
    board_list[move[1]] = board_list[move[0]]
    if move[1] > 27:  # if the destination is on the last row, king the piece if necessary.
        board_list[move[1]] = board_list[move[1]].upper()
    board_list[move[0]] = ' '
    return ''.join(board_list)


#
# Logic for jump moves.
#
def _jump_moves(board):
    """Takes in a board string and return a set of tuples representing legal (non-jump) moves.  It returns a list of the
    path of the checker and all jumped squares so that, for example, if a checker at position 1 jumps checkers a squares
    5 and 13, the returned tuple would be (1, 5, 8, 13, 17).

    Args:
      board: board string

    Returns:
      list of tuples giving path of checker and jumped locations.
    """
    fwd = [t for t in FWD_JUMPS if board[t[0]].lower() == 'b' and board[t[1]].lower() == 'r' and board[t[2]] == ' ']
    bwd = [t for t in BWD_JUMPS if board[t[0]] == 'B' and board[t[1]].lower() == 'r' and board[t[2]] == ' ']
    single_jumps = fwd + bwd
    jumps = []
    for j in single_jumps:
        jumps += tuple(_continue_jump(board, list(j)))
    return jumps


def _continue_jump(board, jump_list):
    """Takes a list representing a jump and returns list of possible continuations.  The input is a list as we want it
    to be mutable.

    Args:
        board: board string.
        jump_list: list of jump move (includes source location and jumped locations)

    Returns:
        list of continuations (a list with a single element containing the input if no continuation is possible).
    """
    continuations = []
    # check for forward continuations
    jumped = set(jump_list[1::2])  # checkers that have already been jumped
    for t in FWD_JUMPS:
        if (t[0] == jump_list[-1] and (board[t[2]] == ' ' or t[2] == jump_list[0]) and t[1] not in jumped and
                    board[t[1]].lower() == 'r'):
            continuations += _continue_jump(board, jump_list + [t[1], t[2]])
    # if piece is a king, check for backward continuations
    if board[jump_list[0]] == 'B':
        for t in BWD_JUMPS:
            if (t[0] == jump_list[-1] and (board[t[2]] == ' ' or t[2] == jump_list[0]) and t[1] not in jumped and
                        board[t[1]].lower() == 'r'):
                continuations += _continue_jump(board, jump_list + [t[1], t[2]])
    if continuations:
        return continuations
    else:
        return [jump_list]


def _apply_jump(board, move):
    """Apply a jump move to a given board.

    Args:
      board: board string
      move: move tuple

    Returns:
      Board string of new position.
    """
    assert (board[move[0]].lower() == 'b')
    board_list = list(board)
    board_list[move[-1]] = board_list[move[0]]
    if move[-1] > 27:  # if the destination is on the last row, king the piece if necessary.
        board_list[move[-1]] = board_list[move[-1]].upper()
    board_list[move[0]] = ' '
    # remove the jumped checkers
    for i in move[1::2]:
        board_list[i] = ' '
    return ''.join(board_list)


def print_board(board):
    """Print the board (purely for help visualizing).

    Args:
        board: board string.
    """
    for r in range(0, 32, 8):
        print '# ---   ---   ---   ---   '
        print '# --- %s --- %s --- %s --- %s ' % (board[r], board[r + 1], board[r + 2], board[r + 3])
        print '# ---   ---   ---   ---   '
        print '#    ---   ---   ---   ---'
        print '#  %s --- %s --- %s --- %s ---' % (board[r + 4], board[r + 5], board[r + 6], board[r + 7])
        print '#    ---   ---   ---   ---'
