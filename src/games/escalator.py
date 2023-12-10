#!/usr/bin/env python3

"""
Escalator Solitaire game

Escalator is a Tri-Peaks style game in which cards are matched to the card
in the waste pile if they are one higher or one lower in rank.

 The game is
won when all cards are removed from the tableau.
Unlike Tri-Peaks, the cards in the tableau are dealt into a single peak, and
the cards on the tableau are all visible.

Rules:
    - Cards are dealt into a single peak.
    - Cards are matched to the card in the waste pile if they are one higher
      or one lower in rank.
    - The game is won when all cards are removed from the tableau.
    - Cards are flipped from the stock pile one at a time to the waste pile.
    - The top card of the waste pile is available for play.

Scoring:
    - 100 points for clearing the tableau.
    - 1 point for each card removed from the tableau.
"""

from src.games._base import SolitaireGame


class EscalatorGame(SolitaireGame):
    """Represents a game of Escalator Solitaire."""
    pass
