import unittest
from math import inf
from connect4 import Board


def alpha_beta(board, player, alpha, beta, max_depth):
    if board.is_terminal():
        return board.game_value(), 0, 0

    if max_depth == 0:
        return 0, 0, 0

    optimal_score = -inf if player == 'X' else inf
    optimal_move = 0
    expansion = 0

    for current_move in board.available_moves():
        board.perform_move(current_move, player)
        max_depth -= 1

        leaf_score, next_player_move, expanded \
            = alpha_beta(board,
                         'O' if player == 'X' else 'X',
                         alpha,
                         beta,
                         max_depth)

        expansion += expanded
        expansion += 1

        board.undo_move(current_move)
        max_depth += 1

        if player == 'X':
            if leaf_score > optimal_score:
                optimal_score = leaf_score
                optimal_move = current_move
            if optimal_score >= beta:
                return optimal_score, current_move, expansion
            alpha = max(alpha, leaf_score)
        else:
            if leaf_score < optimal_score:
                optimal_score = leaf_score
                optimal_move = current_move
            if optimal_score <= alpha:
                return optimal_score, current_move, expansion
            beta = min(beta, optimal_score)

    return optimal_score, optimal_move, expansion


class TestMinMaxDepth1(unittest.TestCase):

    def test_depth1a(self):
        b = Board()
        player = b.create_board('010101')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 1)
        self.assertEqual(bestScore, 1)
        self.assertEqual(bestMove, 0)

    def test_depth1b(self):
        b = Board()
        player = b.create_board('001122')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 1)
        self.assertEqual(bestScore, 1)
        self.assertEqual(bestMove, 3)

    def test_depth1c(self):
        b = Board()
        player = b.create_board('335566')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 1)
        self.assertEqual(bestScore, 1)
        self.assertEqual(bestMove, 4)

    def test_depth1d(self):
        b = Board()
        player = b.create_board('3445655606')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 1)
        self.assertEqual(bestScore, 1)
        self.assertEqual(bestMove, 6)

    def test_depth1e(self):
        b = Board()
        player = b.create_board('34232210101')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 1)
        self.assertEqual(bestScore, -1)
        self.assertEqual(bestMove, 1)

    def test_depth1f(self):
        b = Board()
        player = b.create_board('23445655606')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 1)
        self.assertEqual(bestScore, -1)
        self.assertEqual(bestMove, 6)

    def test_depth1g(self):
        b = Board()
        player = b.create_board('33425614156')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 1)
        self.assertEqual(bestScore, -1)
        self.assertEqual(bestMove, 2)


class TestMinMaxDepth3(unittest.TestCase):

    def test_depth3a(self):
        b = Board()
        player = b.create_board('303111426551')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 3)
        self.assertEqual(bestScore, 1)
        self.assertEqual(bestMove, 2)

    def test_depth3b(self):
        b = Board()
        player = b.create_board('23343566520605001')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 3)
        self.assertEqual(bestScore, -1)
        self.assertEqual(bestMove, 6)

    def test_depth3c(self):
        b = Board()
        player = b.create_board('10322104046663')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 3)
        self.assertEqual(bestScore, 1)
        self.assertEqual(bestMove, 0)

    def test_depth3d(self):
        b = Board()
        player = b.create_board('00224460026466')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 3)
        self.assertEqual(bestScore, 1)
        self.assertEqual(bestMove, 3)

    def test_depth3e(self):
        b = Board()
        player = b.create_board('102455500041526')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 3)
        self.assertEqual(bestScore, -1)
        self.assertEqual(bestMove, 1)

    def test_depth3f(self):
        b = Board()
        player = b.create_board('01114253335255')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 3)
        self.assertEqual(bestScore, 1)
        self.assertEqual(bestMove, 2)

    def test_depth3g(self):
        b = Board()
        player = b.create_board('0325450636643')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 3)
        self.assertEqual(bestScore, -1)
        self.assertEqual(bestMove, 5)


class TestMinMaxDepth5(unittest.TestCase):
    def test_depth5a(self):
        b = Board()
        player = b.create_board('430265511116')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 5)
        self.assertEqual(bestScore, 1)
        self.assertEqual(bestMove, 3)

    def test_depth5b(self):
        b = Board()
        player = b.create_board('536432111330')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 5)
        self.assertEqual(bestScore, 1)
        self.assertEqual(bestMove, 5)

    def test_depth5c(self):
        b = Board()
        player = b.create_board('322411004326')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 5)
        self.assertEqual(bestScore, 1)
        self.assertEqual(bestMove, 3)

    def test_depth5d(self):
        b = Board()
        player = b.create_board('3541226000220')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 5)
        self.assertEqual(bestScore, -1)
        self.assertEqual(bestMove, 4)

    def test_depth5e(self):
        b = Board()
        player = b.create_board('43231033655')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 5)
        self.assertEqual(bestScore, -1)
        self.assertEqual(bestMove, 1)

    def test_depth5f(self):
        b = Board()
        player = b.create_board('345641411335')
        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 5)
        self.assertEqual(bestScore, 1)
        self.assertEqual(bestMove, 5)

    def test_depth5g(self):
        b = Board()
        player = b.create_board('336604464463')

        bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 5)

        self.assertEqual(bestScore, 1)
        self.assertEqual(bestMove, 3)

        print(expansions)


if __name__ == "__main__":
    unittest.main()
