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

    def won():
        self.score += 1

def main(window):
    player = namedtuple("Players", ["X", "O"])(
        Player("X"),
        Player("O")
    )
    current_player = random.choice([player.X, player.O])
    winner = None

    board = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]

    # positions represented as (y,x) coordinates
    cursor_position_matrix = [
        [(6, 4), (6, 6), (6, 8)],
        [(8, 4), (8, 6), (8, 8)],
        [(10, 4), (10, 6), (10, 8)],
    ]

    # referring to the index of the cursor position within the cursor_position_matrix as [a][b]
    # SHOULD BE CONGRUENT WITH THE DATA-STRUCTURE OF THE BOARD
    cursor_position_within_matrix = [0, 0]

    continue_playing = True

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
        while not winner:
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

            cursor_position = cursor_position_matrix[cursor_position_within_matrix[0]][cursor_position_within_matrix[1]]
            window.move(*cursor_position)

            match (key := window.getch()):
                case curses.KEY_UP:
                    cursor_position_within_matrix[0] = (cursor_position_within_matrix[0] - 1) % 3
                case curses.KEY_DOWN:
                    cursor_position_within_matrix[0] = (cursor_position_within_matrix[0] + 1) % 3
                case curses.KEY_LEFT:
                    cursor_position_within_matrix[1] = (cursor_position_within_matrix[1] - 1) % 3
                case curses.KEY_RIGHT:
                    cursor_position_within_matrix[1] = (cursor_position_within_matrix[1] + 1) % 3
                case curses.KEY_ENTER | 10:
                    if board[cursor_position_within_matrix[0]][cursor_position_within_matrix[1]] is None:
                        board[cursor_position_within_matrix[0]][cursor_position_within_matrix[1]] = current_player

                        current_player = player.X if current_player == player.O else player.O

                    for i in range(0, 3):
                        if (board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] is not None):
                            winner = board[i][0]
                            break

                    if not winner:
                        for j in range(0, 3):
                            if (board[0][j] == board[1][j] and board[1][j] == board[2][j] and board[0][j] is not None):
                                winner = board[0][j]
                                break

                    if not winner:
                        if (board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] is not None):
                            winner = board[0][0]

                    if not winner:
                        if (board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] is not None):
                            winner = board[0][2]

                    # draw

            window.refresh()

        # score screen
        if winner:
            winner.score += 1

        curses.curs_set(0)
        window.clear()
        window.box()

        window.addstr(3, 4, "score")

        window.addstr(7, 1, f"{player.X}:{str(player.X.score)}")
        window.addstr(7, 8, f"{player.O}:{str(player.O.score)}")

        if winner:
            window.addstr(9, 3, f"{winner}  won!")

        while True:
            window.addch(12, 4, "x", curses.A_REVERSE if not continue_playing else curses.A_NORMAL)
            window.addch(12, 8, "→", curses.A_REVERSE if continue_playing else curses.A_NORMAL)

            match (key := window.getch()):
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

                    cursor_position_within_matrix = [0, 0]

                    break

wrapper(main)
