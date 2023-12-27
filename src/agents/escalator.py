#!/usr/bin/env python3

"""
Reinformcement Learning Agent for Escalator Solitaire
"""

from pathlib import Path


class EscalatorAgent:
    """
    Agent for playing Escalator Solitaire.

    Offline learning agent.
    """

    def __init__(self, save_itr_count: int):
        """
        Args:
            save_itr_count: The number of iterations between saving the model.
        """

        # The model is saved to checkpoint training progress
        self._iteration = 0
        self._save_itr_count = save_itr_count
        self._save_path = Path("models", "escalator_agent")
        self._save_path.mkdir(parents=True, exist_ok=True)

        # Stateful information
        self._history = []

    def decide_move(self, state: list[list], available_moves: list) -> int:
        """
        Choose an action to take.

        Args:
            game: The game to choose an action for.

        Returns:
            The index of the action to take.
        """

        return 0

    def observe(
        self,
        state: list[list],
        action: int,
        reward: int,
        next_state: list[list],
        is_terminal_state: bool = False,
    ) -> None:
        """
        Observe the result of an action.

        Args:
            state: The state of the game that the action was made.
            action: The action taken.
            reward: The reward for the action.
            next_state: The next state of the game.
            is_terminal_state: Whether the next state is a terminal state.
        """

        # We track all of the moves and states in the game to learn offline
        self._history.append((state, action, reward, next_state))

        # We learn from the final results of the game
        if is_terminal_state:
            self.learn()
            self._history.clear()

    def learn(self) -> None:
        """
        Learn from the observed results.
        """

        # Learn the effects of actions towards final state
        for state, action, reward, next_state in reversed(self._history):
            pass

        # Save the model every so often
        self._iteration += 1
        if self._iteration % self._save_itr_count == 0:
            self.save_model()

    def save_model(self) -> None:
        """
        Save the model.
        """

        pass
