#!/usr/bin/env python3

"""
Base game class

This module provides a base class for all solitaire games.
The standard construction of a solitaire game has a;
- Stock pile,
    - These are cards which are not yet in play.
    - None of these are visible by convention.
    - Some games might not have a stock pile.
- Waste pile,
    - Cards taken from the stock pile.
    - These cards are always visible by convention.
    - Some games have more than one card in the Waste pile, but only the top
    most card is playable.
    - Some games do not have a Waste pile as the Stock is immediately played
    to the Tableau
- Tableau,
    - Cards in the main playing area.
    - The exact construction of this area will differ with every game.
    - Some games allow for multiple cards to be moved at once if they satisfy
    some sequence.
- Foundation, and
    - Cards that are in the "goal" position.
- Reserve,
    - Cards that are reserved and can be drawn from.
    - Some varients of Solitaire combine the Foundation and Reserve piles.

Most games allow for the stock to be flipped back over and reused a number of
times.

The common game workflow is as follows;
- Initial setup / deal
- Loop:
- Player moves
- Update game state
- Score update
- Check for win/loss and return if so
- Else, jump Loop
"""


class Card:
    """
    Represents a playing card.
    """

    RANKS = ["NONE", "A"] + [str(i) for i in range(2, 11)] + ["J", "Q", "K"]
    SUITS = [
        "\N{BLACK SPADE SUIT}",
        "\N{BLACK CLUB SUIT}",
        "\N{BLACK HEART SUIT}",
        "\N{BLACK DIAMOND SUIT}",
    ]

    def __init__(self, rank: int, suit: int, visible: bool = False):
        """
        Args:
            rank: The numeric value of the card
            suit: The suit of the card (index into )
            visible: Whether the card is has the playing side facing up
        """

        # Sanity checks
        if rank < 1 or rank > 13:
            raise ValueError("Rank must be between 1 and 13")
        if suit < 0 or suit > 3:
            raise ValueError("Suit must be between 0 and 3")

        self._rank = rank
        self._suit = suit
        self._visible = visible

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def suit(self) -> int:
        return self._suit

    @property
    def visible(self) -> bool:
        return self._visible

    def __str__(self) -> str:
        str_rank = Card.RANKS[self._rank]
        str_suit = Card.SUITS[self._suit]
        return f"{str_rank}{str_suit}"

    def flip(self):
        self._visible = True

    def hide(self):
        self._visible = False


class SolitaireGame:
    """
    Base class for all solitaire games.
    """

    def __init__(self):
        self._stock: list[Card] = []
        self._waste: list[Card] = []
        self._tableau: list[list[Card]] = []
        self._foundation: list[list[Card]] = []
        self._reserve: list[Card] = []
        self._available_moves: list[tuple[int, int]] = []
        self._restock_cycle_remaining = 0

    @property
    def in_winning_state(self) -> bool:
        """
        Default condition for winning
        """
        return len(self._tableau) == 0

    @property
    def in_losing_state(self) -> bool:
        """
        Default condition for losing
        """
        return len(self._available_moves) == 0

    @property
    def stock(self) -> list[Card]:
        return self._stock

    @property
    def waste(self) -> list[Card]:
        return self._waste

    @property
    def tableau(self) -> list[list[Card]]:
        return self._tableau

    @property
    def foundation(self) -> list[list[Card]]:
        return self._foundation

    @property
    def reserve(self) -> list[Card]:
        return self._reserve

    @property
    def available_moves(self) -> list[tuple[int, int]]:
        """
        A move is a tuple of two integers, the first being the index of the
        operand, and the second being the index of the destination.
        """
        return self._available_moves

    @property
    def restock_cycle_remaining(self) -> int:
        return self._restock_cycle_remaining

    def update_available_moves(self) -> None:
        """
        Update the list of available moves.
        """
        raise NotImplementedError(
            "_update_available_moves() must be implemented by subclasses to "
            "update the list of available moves."
        )

    def deal(
        self,
        stock: list[Card] | None = None,
        waste: list[Card] | None = None,
        tableau: list[list[Card]] | None = None,
        foundation: list[list[Card]] | None = None,
        reserve: list[Card] | None = None,
    ) -> None:
        """
        This method should be overridden by subclasses to set the game up.

        A given state of the game should be able to be provided here for;
        - Testing
        - User saved games (idk)
        - AI training

        Args:
            stock: The stock pile
            waste: The waste pile
            tableau: The tableau
            foundation: The foundation
        """
        raise NotImplementedError(
            "deal() must be implemented by subclasses to set up the game."
        )

    def move(self, source: int, destination: int) -> int:
        """
        The Agent / User makes an effect on the world state.

        The options for moves, or actions, are as follows;
        - Flip Stock to Waste (or cycle Stock if depleted),
        - Stack Waste on a card or space in the Tableau,
        - Stack card, or sequecen, in Tableau on another card in the Tableau,
        - Place card into the Reserve,
        - Stack card from Reserve onto Tableau,
        - Place card into Foundation,

        These may need to be separate methods to call, which will require the
        Agent to decode it's own output into a clear action to perform here.
        This will decouple the construction of the network from the
        implementation of the game.
        Alternatively, each game has a specific method of decoding an input
        value (or sequence) into an action to affect on the world state.
        This will enforce a standard definition of an Agents action,
        presumably being a tuple of values that define and index of an operand
        and a location to move it to, which will allow for more direct
        comparison between algorithms.
        Really, these two points are not mutually exclusive.

        This method should be overridden by subclasses to implement the game
        logic.

        Args:
            move: The move to make

        Returns:
            The score for the move

        Raises:
            ValueError: If the move is invalid
        """
        raise NotImplementedError(
            "move() must be implemented by subclasses to implement the game"
            " logic."
        )
