#!/usr/bin/env python3

"""
Testing the base / abstract class for the world
"""

import unittest
from src.games._base import Card


class TestCard(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
