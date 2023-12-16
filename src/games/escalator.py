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
    - Whilst there is no visible foundation, it can be thought that any card
    that is removed from the pyramid has been put into the foundation and
    cannot be retrieved. This is a way to track what has already been removed.

Scoring:
    - 100 points for clearing the tableau.
    - 1 point for each card removed from the tableau.
    TODO: find the scoring that Gnome does, and then see what the affect on
    the model training and accuracy is when scoring with something that say
    multiplies the score based on the chain of cards removed.
"""

from random import shuffle

from src.games.base import SolitaireGame, Card


class EscalatorGame(SolitaireGame):
    """Represents a game of Escalator Solitaire."""

    def __init__(self):
        super().__init__()
        self.foundation.append([])  # Only one foundation pile

    @property
    def in_winning_state(self) -> bool:
        return len(self._tableau) == 0

    def deal(
        self,
        stock: list[Card] | None = None,
        waste: list[Card] | None = None,
        tableau: list[list[Card]] | None = None,
        foundation: list[list[Card]] | None = None,
        reserve: list[Card] | None = None,
    ) -> None:
        """
        Deal the game.

        Args:
            stock: The stock pile.
            waste: The waste pile.
            tableau: The tableau.
            foundation: The foundation.
            reserve: The reserve pile.
        """

        if None not in (stock, waste, tableau, foundation, reserve):
            # NOTE: No sanity checks here
            self.stock.extend(stock)
            self.waste.extend(waste)
            self.tableau.extend(tableau)
            self.foundation.extend(foundation)
            self.reserve.extend(reserve)
            return

        # If everything hasn't been given, then we must deal the game
        # according to the rules.
        deck = EscalatorGame.create_deck()
        shuffle(deck)
        for i in range(7):
            # 7 rows of the tableau
            row = deck[:i + 1]
            deck = deck[i + 1:]
            self.tableau.append(row)

            # The cards in the tableau are visible
            for card in row:
                card.flip()

        self.stock.extend(deck)
        self.update_available_moves()

    def display(self) -> str:
        """
        Display the game.
        """

        # First the stock and waste piles
        stock_and_waste = "{} {}".format(
            self.stock[-1] if len(self.stock) != 0 else "[  ]",
            self.waste[-1] if len(self.waste) != 0 else "[  ]",
        )

        # Next, every row of the tableau
        tableau = "\n".join(
            "  ".join(
                str(card)
                if card is not None
                else "[  ]"
                for card in row
            ).center(4 * 7 + 6 * 2 - 1)
            for row in self.tableau
        )

        # As the remainder of the piles are not visible, we return
        return "\n".join(
            (stock_and_waste, tableau)
        )

    def move(self, destination: int) -> int:
        """
        The Agent / User makes an effect on the world state.

        The options for moves, or actions, are as follows;
        - Flip Stock to Waste (or cycle Stock if depleted),
        - Stack Waste on a card in the Tableau,

        Stacking a card from the waste onto the tableau removes that waste
        card and replaces it with the card from the tableau.
        This space is then empty.

        Args:
            destination: The index of the destination to move to

        Returns:
            The score for the move

        Raises:
            ValueError: If the move is invalid
        """

        reward = 0

        if (0, destination) not in self.available_moves:
            raise ValueError("Invalid move")

        if destination == 0:
            # Flip stock to waste
            if len(self.stock) == 0:
                # No more cards to flip
                raise ValueError("Invalid move")

            if len(self.waste) == 0:
                self.waste.append(None)
            self.waste[0] = self.stock.pop()
            self.waste[0].flip()
        else:
            # Decode the destination, or flip the stock
            row = destination // 10 - 1
            idx = destination % 10 - 1

            # Waste card goes to foundation
            self.foundation[0].append(self.waste[0])

            # Tableau card goes to waste
            self.waste[0] = self.tableau[row][idx]

            # Tableau card slot is emptied
            self.tableau[row][idx] = None

            reward = 1

        self.update_available_moves()
        return reward

    def update_available_moves(self) -> None:
        """
        Update the list of available moves.
        """

        self.available_moves.clear()

        # Check for stock flip
        if len(self.stock) != 0:
            self.available_moves.append((0, 0))

        # Check which cards the waste can be stacked on
        if len(self.waste) != 0:
            rank = self.waste[0].rank
            stack_up = rank + 1
            stack_down = rank - 1
            if stack_up == 14:
                stack_up = 1
            if stack_down == 0:
                stack_down = 13

            for row in range(len(self.tableau)):
                for col in range(len(self.tableau[row])):
                    tab_card = self.tableau[row][col]
                    if tab_card is not None:
                        if (
                            tab_card.rank == stack_up
                            or tab_card.rank == stack_down
                        ):
                            self.available_moves.append(
                                (0, (row + 1) * 10 + col + 1)
                            )
