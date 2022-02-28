#! /usr/bin/env python3

from collections import namedtuple
from curses import wrapper
import curses
import random

class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0

    def __hash__(self):
        return hash((self.name))

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        elif other is None:
            return False
        else:
            raise TypeError(f"Type '{type(other).__name__}' cannot be compared to type '{type(self).__name__}'")

    def __ne__(self, other):
        return not(self == other)

    def __str__(self):
        return self.name


def game(window):
    DRAW_GAME = 'draw'

    continue_playing = True

    winner = None

    player = namedtuple("Players", ["X", "O"])(
        Player("X"),
        Player("O")
    )

    current_player = random.choice([player.X, player.O])

    # referring to the indices of the cursor position within cursor_position
    metaposition = [0, 0]

    # positions represented as (y,x) coordinates
    cursor_position = [
        [(6, 4), (6, 6), (6, 8)],
        [(8, 4), (8, 6), (8, 8)],
        [(10, 4), (10, 6), (10, 8)],
    ]

    board = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]

    # initialize window
    curses.resizeterm(15, 13)
    curses.curs_set(0)
    window.getch()

    # splash screen
    window.clear()
    window.box()

    window.addstr(6, 2, "tic")
    window.addstr(7, 5, "tac")
    window.addstr(8, 8, "toe")

    window.addstr(12, 4, "[ → ]", curses.A_BLINK)

    window.refresh()
    window.getch()


    while continue_playing:
        # game screen
        while (not winner) and (winner != DRAW_GAME):
            window.clear()
            window.box()

            # scores
            window.addstr(2, 2, f"{player.X}:{str(player.X.score)}", curses.A_REVERSE if current_player == player.X else curses.A_NORMAL)
            window.addstr(2, 8, f"{player.O}:{str(player.O.score)}", curses.A_REVERSE if current_player == player.O else curses.A_NORMAL)

            # board
            window.addstr(6, 4, f"{board[0][0] or ' '}|{board[0][1] or ' '}|{board[0][2] or ' '}")
            window.addstr(7, 4, f"-+-+-")
            window.addstr(8, 4, f"{board[1][0] or ' '}|{board[1][1] or ' '}|{board[1][2] or ' '}")
            window.addstr(9, 4, f"-+-+-")
            window.addstr(10, 4, f"{board[2][0] or ' '}|{board[2][1] or ' '}|{board[2][2] or ' '}")

            curses.curs_set(1)

            window.move(*cursor_position[metaposition[0]][metaposition[1]])

            match window.getch():
                case curses.KEY_UP:
                    metaposition[0] = (metaposition[0] - 1) % 3
                case curses.KEY_DOWN:
                    metaposition[0] = (metaposition[0] + 1) % 3
                case curses.KEY_LEFT:
                    metaposition[1] = (metaposition[1] - 1) % 3
                case curses.KEY_RIGHT:
                    metaposition[1] = (metaposition[1] + 1) % 3
                case curses.KEY_ENTER | 10:
                    if board[metaposition[0]][metaposition[1]] is None:
                        board[metaposition[0]][metaposition[1]] = current_player

                        current_player = player.X if current_player == player.O else player.O

                    for i in range(0, 3):
                        if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] is not None:
                            winner = board[i][0]
                            break

                        if board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] is not None:
                            winner = board[0][i]
                            break

                    if ((board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[1][1] is not None) or
                        (board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[1][1] is not None)
                    ):
                        winner = board[1][1]
                        break

                    if len(list(filter(lambda a: a == player.X or a == player.O, (board[i][j] for i in range(3) for j in range(3))))) == 9:
                        winner = DRAW_GAME
                        break

            window.refresh()

        # score screen
        if winner and (winner != DRAW_GAME):
            winner.score += 1

        curses.curs_set(0)
        window.clear()
        window.box()

        window.addstr(3, 4, "score")

        window.addstr(7, 2, f"{player.X}:{str(player.X.score)}")
        window.addstr(7, 8, f"{player.O}:{str(player.O.score)}")

        if winner != DRAW_GAME:
            window.addstr(9, 3, f"{winner}  won!")

        while True:
            window.addch(12, 4, "x", curses.A_REVERSE if not continue_playing else curses.A_NORMAL)
            window.addch(12, 8, "→", curses.A_REVERSE if continue_playing else curses.A_NORMAL)

            match window.getch():
                case curses.KEY_LEFT | curses.KEY_RIGHT:
                    continue_playing = False if continue_playing else True
                    window.refresh()

                case curses.KEY_ENTER | 10:
                    if not continue_playing:
                        return

                    winner = None

                    current_player = random.choice([player.X, player.O])

                    board = [
                        [None, None, None],
                        [None, None, None],
                        [None, None, None],
                    ]

                    metaposition = [0, 0]

                    break


if __name__ == '__main__':
    wrapper(game)
