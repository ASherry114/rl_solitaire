#!/usr/bin/env python3

"""
Testing the base / abstract class for the world
"""

import unittest
from src.games._base import Card


class TestCard(unittest.TestCase):
    def test_card_properties(self):
        card = Card(2, 1, True)
        self.assertEqual(card.rank, 2)
        self.assertEqual(card.suit, 1)
        self.assertEqual(card.visible, True)

    def test_card_flip(self):
        card = Card(3, 0)
        self.assertEqual(card.visible, False)
        card.flip()
        self.assertEqual(card.visible, True)
        card.flip()
        self.assertEqual(card.visible, True)

    def test_card_hide(self):
        card = Card(4, 3, True)
        self.assertEqual(card.visible, True)
        card.hide()
        self.assertEqual(card.visible, False)
        card.hide()
        self.assertEqual(card.visible, False)

    def test_card_string_representation(self):
        card = Card(1, 2)
        self.assertEqual(str(card), "A\N{BLACK HEART SUIT}")


if __name__ == "__main__":
    unittest.main()
