"""Tests associated with the moves module to determine legal checkers
moves.
"""

__author__ = 'lhurd'

import moves
import unittest

# ---   ---   ---   ---
# --- b --- b --- b --- b
# ---   ---   ---   ---
#    ---   ---   ---   ---
#  b --- b --- b --- b ---
#    ---   ---   ---   ---
# ---   ---   ---   ---
# --- b --- b --- b --- b
# ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
# ---   ---   ---   ---
# ---   ---   ---   ---
# ---   ---   ---   ---
#    ---   ---   ---   ---
#  r --- r --- r --- r ---
#    ---   ---   ---   ---
# ---   ---   ---   ---
# --- r --- r --- r --- r
# ---   ---   ---   ---
#    ---   ---   ---   ---
#  r --- r --- r --- r ---
#    ---   ---   ---   ---
STARTING_BOARD = 'bbbbbbbbbbbb        rrrrrrrrrrrr'

# ---   ---   ---   ---
# ---   ---   ---   ---
# ---   ---   ---   ---
#    ---   ---   ---   ---
#    --- b ---   ---   ---
#    ---   ---   ---   ---
# ---   ---   ---   ---
# ---   --- r ---   ---
# ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   --- b ---
#    ---   ---   ---   ---
# ---   ---   ---   ---
# ---   ---   --- r ---
# ---   ---   ---   ---
#    ---   ---   ---   ---
#    --- b ---   ---   ---
#    ---   ---   ---   ---
# ---   ---   ---   ---
# --- r ---   --- r ---
# ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   --- B ---   ---
#    ---   ---   ---   ---
TEST_BOARD1 = '     b   r     b  r  b  r r   B '

# ---   ---   ---   ---
# ---   ---   ---   ---
# ---   ---   ---   ---
#    ---   ---   ---   ---
#    --- b ---   ---   ---
#    ---   ---   ---   ---
# ---   ---   ---   ---
# ---   --- r ---   ---
# ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
# ---   ---   ---   ---
# ---   --- r --- r ---
# ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
# ---   ---   ---   ---
# --- r ---   ---   ---
# ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
TEST_BOARD2 = '     b   r       rr     r       '

# ---   ---   ---   ---
# ---   ---   ---   ---
# ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
# ---   ---   ---   ---
# ---   ---   ---   ---
# ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
# ---   ---   ---   ---
# --- r --- r --- R ---
# ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
# ---   ---   ---   ---
# --- r --- r --- R ---
# ---   ---   ---   ---
#    ---   ---   ---   ---
#    --- B ---   ---   ---
#    ---   ---   ---   ---
TEST_BOARD3 = '                rrR     rrR  B  '

# ---   ---   ---   ---
# ---   ---   ---   ---
# ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
# ---   ---   ---   ---
# ---   ---   ---   ---
# ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
# ---   ---   ---   ---
# --- r --- r --- r ---
# ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
#    ---   ---   ---   ---
# ---   ---   ---   ---
# --- r --- r ---   ---
# ---   ---   ---   ---
#    ---   ---   ---   ---
#    --- B ---   ---   ---
#    ---   ---   ---   ---
TEST_BOARD4 = '                rrr     rr   B  '


class MovesTest(unittest.TestCase):
    def test_children(self):
        self.assertItemsEqual(['bbbbbbbb bbbb       rrrrrrrrrrrr',
                               'bbbbbbbb bbb b      rrrrrrrrrrrr',
                               'bbbbbbbbb bb b      rrrrrrrrrrrr',
                               'bbbbbbbbb bb  b     rrrrrrrrrrrr',
                               'bbbbbbbbbb b  b     rrrrrrrrrrrr',
                               'bbbbbbbbbb b   b    rrrrrrrrrrrr',
                               'bbbbbbbbbbb    b    rrrrrrrrrrrr'],
                              moves.find_children(STARTING_BOARD))
        self.assertItemsEqual(['               b     b br r   B ',
                               '     b   r           b  r     BB',
                               '     b   r     b  r       r B B ',
                               '     b   r    Bb     b  r       '],
                              moves.find_children(TEST_BOARD1))

    def test_flip(self):
        self.assertEqual('bbbb    bbbb        rrrrrrrrrrrr',
                         moves.flip('bbbbbbbbbbbb        rrrr    rrrr'))
        self.assertEqual('BBBB    BBBB        RRRRRRRRRRRR',
                         moves.flip('BBBBBBBBBBBB        RRRR    RRRR'))

    def test_normal_moves(self):
        self.assertItemsEqual([(5, 8), (15, 19), (21, 25), (30, 25)],
                              moves._normal_moves(TEST_BOARD1))

    def test_apply_move(self):
        # forward move (normal checker).
        self.assertEqual('bbbbbbbbb bb  b     rrrrrrrrrrrr',
                         moves._apply_move(STARTING_BOARD, (9, 14)))
        # forward move (normal checker with promotion).
        self.assertEqual('    rrrr                 bbb B  ',
                         moves._apply_move('    rrrr                bbbb    ',
                                           (24, 29)))
        # forward move (king).
        self.assertEqual('bbbbbbbbb bb  B     rrrrrrrrrrrr',
                         moves._apply_move('bbbbbbbbbBbb        rrrrrrrrrrrr',
                                           (9, 14)))
        # forward move (king) to last rank.
        self.assertEqual('    rrrr                 bbb B  ',
                         moves._apply_move('    rrrr                Bbbb    ',
                                           (24, 29)))
        # backward move (king).
        self.assertEqual('    rrrr                Bbbb    ',
                         moves._apply_move('    rrrr                 bbb B  ',
                                           (29, 24)))

    def test_jump_moves(self):
        self.assertItemsEqual([[5, 9, 14, 18, 23], [15, 18, 22, 26, 31],
                               [21, 24, 28], [30, 26, 23, 18, 14]],
                              moves._jump_moves(TEST_BOARD1))
        self.assertItemsEqual([[5, 9, 14, 17, 21, 24, 28], [5, 9, 14, 18, 23]],
                              moves._jump_moves(TEST_BOARD2))
        self.assertItemsEqual([[29, 24, 20, 16, 13, 17, 22, 25, 29],
                               [29, 24, 20, 16, 13, 17, 22, 26, 31],
                               [29, 24, 20, 16, 13, 17, 22, 18, 15],
                               [29, 25, 22, 26, 31],
                               [29, 25, 22, 17, 13, 16, 20, 24, 29],
                               [29, 25, 22, 18, 15]],
                              moves._jump_moves(TEST_BOARD3))
        # An explicit test to make sure that the program does not jump
        # the same checker more than once.  If it were able to jump
        # position 25 twice, it would enable black to capture all five
        # red checkers which doesn't happen,
        self.assertItemsEqual([[29, 24, 20, 16, 13, 17, 22, 25, 29],
                               [29, 24, 20, 16, 13, 17, 22, 18, 15],
                               [29, 25, 22, 17, 13, 16, 20, 24, 29],
                               [29, 25, 22, 18, 15]],
                              moves._jump_moves(TEST_BOARD4))

    def test_continue_jump(self):
        self.assertItemsEqual([[5, 9, 14, 18, 23]],
                              moves._continue_jump(TEST_BOARD1, [5, 9, 14]))
        self.assertItemsEqual([[15, 18, 22, 26, 31]],
                              moves._continue_jump(TEST_BOARD1, [15, 18, 22]))
        self.assertItemsEqual([[21, 24, 28]],
                              moves._continue_jump(TEST_BOARD1, [21, 24, 28]))
        self.assertItemsEqual([[30, 26, 23, 18, 14]],
                              moves._continue_jump(TEST_BOARD1, [30, 26, 23]))
        self.assertItemsEqual([[5, 9, 14, 17, 21, 24, 28], [5, 9, 14, 18, 23]],
                              moves._continue_jump(TEST_BOARD2, [5, 9, 14]))
        self.assertItemsEqual([[29, 25, 22, 26, 31],
                               [29, 25, 22, 17, 13, 16, 20, 24, 29],
                               [29, 25, 22, 18, 15]],
                              moves._continue_jump(TEST_BOARD3, [29, 25, 22]))

    def test_apply_jump(self):
        # forward jump (normal checker).
        self.assertEqual('              bb  r  b  r r   B ',
                         moves._apply_jump(TEST_BOARD1, (5, 9, 14)))
        # forward jump (normal checker with promotion).
        self.assertEqual('     b   r     b  r       r B B ',
                         moves._apply_jump(TEST_BOARD1, (21, 24, 28)))
        # forward multiple jump (normal checker with promotion).
        self.assertEqual('     b   r           b  r     BB',
                         moves._apply_jump(TEST_BOARD1, (15, 18, 22, 26, 31)))
        # backward jump (king).
        self.assertEqual('     b   r    Bb     b  r       ',
                         moves._apply_jump(TEST_BOARD1, (30, 26, 23, 18, 14)))


if __name__ == '__main__':
    unittest.main()
