#!/usr/bin/env python3

from src.games.escalator import EscalatorGame


if __name__ == "__main__":

    def clear_screen():
        print("\033c", end="")
        # print("\033[H\033[J", end="")

    def move_cursor_up(n):
        print("\033[{}A".format(n), end="")

    game = EscalatorGame()
    game.deal()
    num_lines = game.display().count("\n") + 1

    while not (game.in_winning_state or game.in_losing_state):
        # Display
        clear_screen()
        print(game.display())
        print()
        print([move[1] for move in game.available_moves])
        move = int(input("Move: "))
        game.move(move)
        move_cursor_up(num_lines + 3)

    print(game.display())
    print()
    print()
    print(f"Game over! You {'won' if game.in_winning_state else 'lost'}!")
