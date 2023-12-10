#!/usr/bin/env python3

"""
Testing the base / abstract class for the world
"""

import unittest
from src.games.base import Card, SolitaireGame


class TestCard(unittest.TestCase):
    """
    As the Card class is not to be subclassed, this will be the extent of the
    tests against it.
    """
    def test_card_properties(self):
        """
        Capture changes in constructor order
        """
        card = Card(2, 1, True)
        self.assertEqual(card.rank, 2)
        self.assertEqual(card.suit, 1)
        self.assertEqual(card.visible, True)

    def test_card_flip(self):
        """
        Test that the card is flipped from not visible to visible
        """
        card = Card(3, 0)
        self.assertEqual(card.visible, False)
        card.flip()
        self.assertEqual(card.visible, True)
        card.flip()
        self.assertEqual(card.visible, True)

    def test_card_hide(self):
        """
        Test that the card is hidden from visible to not visible
        """
        card = Card(4, 3, True)
        self.assertEqual(card.visible, True)
        card.hide()
        self.assertEqual(card.visible, False)
        card.hide()
        self.assertEqual(card.visible, False)

    def test_valid_card_string_representation(self):
        """
        This may seem a redundant test due to using the Card classes own
        lists of the suits and ranks, but this is to ensure that the
        representation of the card is always the same, even if the lists
        change.
        This is also to capture if the range of the ranks or suits changes.
        """
        for rank in range(1, 14):
            for suit in range(4):
                card = Card(rank, suit)
                self.assertEqual(
                    str(card),
                    f"{Card.RANKS[rank]}{Card.SUITS[suit]}"
                )

    def test_invalid_card_rank(self):
        """
        Capture if the range of the valid inputs change
        """
        with self.assertRaises(ValueError):
            Card(0, 1)
        with self.assertRaises(ValueError):
            Card(14, 1)
        with self.assertRaises(ValueError):
            Card(1, -1)
        with self.assertRaises(ValueError):
            Card(1, 4)


class TestSolitaireGame(unittest.TestCase):
    """
    The SolitaireGame class is an abstract class.
    These tests highlight the standard configuration of a Solitaire game
    varient.
    Some of these tests will make assertions which will not be satisfied
    for child classes.
    """
    def test_in_winning_state(self):
        """
        Standard winning state is an empty Tableau, Stock, and Waste.
        In most games, the Foundation (the goal) will be filled in the same
        move the Tableau will be cleared.
        As such, the Foundation is not checked (the nature of a full
        Foundation is specific to a game).
        """
        game = SolitaireGame()
        game._available_moves = []
        game._tableau = []
        game._waste = []
        game._stock = []
        self.assertTrue(game.in_winning_state)
        self.assertFalse(game.in_losing_state)

    def test_in_losing_state(self):
        """
        Standard losing state is a non-empty Tableau, Stock, or Waste,
        with no available moves.
        """
        game = SolitaireGame()
        game._available_moves = []
        game._tableau = [[None]]
        game._waste = []
        game._stock = []
        self.assertTrue(game.in_losing_state)
        self.assertFalse(game.in_winning_state)
        game._tableau = []
        game._waste = [[None]]
        self.assertTrue(game.in_losing_state)
        self.assertFalse(game.in_winning_state)
        game._waste = []
        game._stock = [[None]]
        self.assertTrue(game.in_losing_state)
        self.assertFalse(game.in_winning_state)

    def test_in_neither_state(self):
        """
        Moves are available, and the game is not won or lost.
        """
        game = SolitaireGame()
        game._available_moves = [(None, None)]
        game._tableau = [[None]]
        game._waste = []
        game._stock = []
        self.assertFalse(game.in_losing_state)
        self.assertFalse(game.in_winning_state)
        game._tableau = []
        game._waste = [[None]]
        self.assertFalse(game.in_losing_state)
        self.assertFalse(game.in_winning_state)
        game._waste = []
        game._stock = [[None]]
        self.assertFalse(game.in_losing_state)
        self.assertFalse(game.in_winning_state)


if __name__ == "__main__":
    unittest.main()
