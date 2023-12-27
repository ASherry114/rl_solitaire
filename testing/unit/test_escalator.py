#!/usr/bin/env python3

"""
Test src/games/escalator.py

Escalator Solitaire game
"""

import unittest
from src.games.base import Card
from src.games.escalator import EscalatorGame


class TestEscalator(unittest.TestCase):
    """
    Test the Escalator Solitaire game
    """

    def test_deal_piles_sizes(self):
        """
        Test that the size of the piles are correct for the auto deal
        """

        game = EscalatorGame()
        game.deal()
        self.assertEqual(len(game.reserve), 0)
        self.assertEqual(len(game.foundation), 0)
        self.assertEqual(len(game.stock), 24)
        self.assertEqual(len(game.waste), 0)
        self.assertEqual(len(game.tableau), 7)  # 7 row tall pyramid
        tableau_count = 0
        for pile in game.tableau:
            tableau_count += len(pile)
        self.assertEqual(tableau_count, 28)

    def test_deal_all_tableau_cards_visible(self):
        """
        Test that all cards in the tableau are visible for the auto deal.
        """

        game = EscalatorGame()
        game.deal()
        for pile in game.tableau:
            for card in pile:
                self.assertEqual(card.visible, True)

    def test_deal_no_repeating_cards(self):
        """
        Test that there are no repeating cards in the auto deal.
        """

        game = EscalatorGame()
        game.deal()
        all_cards = []
        for pile in game.tableau:
            for card in pile:
                all_cards.append(card)
        for card in game.stock:
            all_cards.append(card)
        for card in all_cards:
            self.assertEqual(len(all_cards), len(set(all_cards)))

    def test_encoded_state(self):
        """
        Test that the encoded state is correct.
        """

        game = EscalatorGame()
        flat_tableau = []
        curr_rank = 1
        curr_suit = 0
        for _ in range(28):
            flat_tableau.append(
                Card(rank=curr_rank, suit=curr_suit, visible=True)
            )
            curr_suit += 1
            if curr_suit == 4:
                curr_suit = 0
                curr_rank += 1
        game.deal(
            stock=[None] * 24,
            waste=[],
            tableau=[
                flat_tableau[0:1],
                flat_tableau[1:3],
                flat_tableau[3:6],
                flat_tableau[6:10],
                flat_tableau[10:15],
                flat_tableau[15:21],
                flat_tableau[21:28],
            ],
            foundation=[],
            reserve=[],
        )
        encoded_state = game.encode()
        self.assertEqual(len(encoded_state), 52)
        for card in encoded_state:
            self.assertEqual(len(card), 2)
