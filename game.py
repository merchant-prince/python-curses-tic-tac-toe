from curses import wrapper
import curses
import random

def main(window):
    score = {
        "x": 0,
        "o": 0
    }

    turn = random.choice(["x", "o"])

    winner = None

    board = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
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

    next_ = "c"

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


    while next_ == "c":
        # game screen
        while not winner:
            window.clear()
            window.box()

            # scores
            window.addstr(2, 2, f"x:{str(score['x'])}", curses.A_REVERSE if turn == "x" else curses.A_NORMAL)
            window.addstr(2, 8, f"o:{str(score['o'])}", curses.A_REVERSE if turn == "o" else curses.A_NORMAL)

            # board
            window.addstr(6, 4, f"{board[0][0]}|{board[0][1]}|{board[0][2]}")
            window.addstr(7, 4, f"-+-+-")
            window.addstr(8, 4, f"{board[1][0]}|{board[1][1]}|{board[1][2]}")
            window.addstr(9, 4, f"-+-+-")
            window.addstr(10, 4, f"{board[2][0]}|{board[2][1]}|{board[2][2]}")

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
                    if board[cursor_position_within_matrix[0]][cursor_position_within_matrix[1]] == " ":
                        board[cursor_position_within_matrix[0]][cursor_position_within_matrix[1]] = turn
                        turn = "x" if turn == "o" else "o"

                    for i in range(0, 3):
                        if (board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != " "):
                            winner = board[i][0]
                            break

                    if not winner:
                        for j in range(0, 3):
                            if (board[0][j] == board[1][j] and board[1][j] == board[2][j] and board[0][j] != " "):
                                winner = board[0][j]
                                break

                    if not winner:
                        if (board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != " "):
                            winner = board[0][0]

                    if not winner:
                        if (board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] != " "):
                            winner = board[0][2]

                    # draw

            window.refresh()

        # score screen
        if winner:
            score[winner] += 1

        curses.curs_set(0)
        window.clear()
        window.box()

        window.addstr(3, 4, "score")

        window.addstr(7, 1, f"x:{str(score['x'])}")
        window.addstr(7, 8, f"{str(score['o'])}:o")

        if winner:
            window.addstr(9, 3, f"{winner}  won!")

        while True:
            window.addch(12, 4, "c", curses.A_REVERSE if next_ == "c" else curses.A_NORMAL)
            window.addch(12, 8, "e", curses.A_REVERSE if next_ == "e" else curses.A_NORMAL)

            match (key := window.getch()):
                case curses.KEY_LEFT | curses.KEY_RIGHT:
                    next_ = 'c' if next_ == 'e' else 'e'
                    window.refresh()

                case curses.KEY_ENTER | 10:
                    if next_ == 'e':
                        return

                    winner = None
                    turn = "x"

                    board = [
                        [" ", " ", " "],
                        [" ", " ", " "],
                        [" ", " ", " "]
                    ]

                    cursor_position_within_matrix = [0, 0]

                    break

wrapper(main)
