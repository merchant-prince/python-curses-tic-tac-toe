from curses import wrapper
import curses

WIDTH = 13
HEIGHT = 15

def main(window):
    # init
    curses.resizeterm(HEIGHT, WIDTH)
    curses.curs_set(0)
    window.getch()

    # splash screen
    window.clear()
    window.box()

    window.addstr(6, 2, "tic")
    window.addstr(7, 5, "tac")
    window.addstr(8, 8, "toe")

    window.addstr(HEIGHT - 2, 3, "[enter]", curses.A_BLINK)

    window.refresh()
    window.getch()


    # choice screen
    window.clear()
    window.box()

    window.addstr(6, 3, "choose:")

    window.addch(8, 4, "x")
    window.addch(8, 8, "o")

    selected_glyph = 'x'

    while True:
        if selected_glyph == 'x':
            window.addch(8, 4, "x", curses.A_REVERSE)
            window.addch(8, 8, "o")
        else:
            window.addch(8, 4, "x")
            window.addch(8, 8, "o", curses.A_REVERSE)

        match (key := window.getch()):
            case curses.KEY_LEFT | curses.KEY_RIGHT:
                selected_glyph = 'o' if selected_glyph == 'x' else 'x'

            case curses.KEY_ENTER | 10:
                """
                apparently curses.KEY_ENTER is unreliable.
                pressing the 'Enter' key yields the keycode 10.
                using both for a more consistent result.
                """
                break

        window.refresh()

    score = {
        "x": 0,
        "o": 0
    }

    turn = "x"

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

    # game screen
    while not winner:
        window.clear()
        window.box()

        # scores
        window.addch(2, 2, "x", curses.A_REVERSE if turn == "x" else curses.A_NORMAL)
        window.addch(2, 3, ":", curses.A_REVERSE if turn == "x" else curses.A_NORMAL)
        window.addch(2, 4, str(score["x"]), curses.A_REVERSE if turn == "x" else curses.A_NORMAL)

        window.addch(2, 8, str(score["o"]), curses.A_REVERSE if turn == "o" else curses.A_NORMAL)
        window.addch(2, 9, ":", curses.A_REVERSE if turn == "o" else curses.A_NORMAL)
        window.addch(2, 10, "o", curses.A_REVERSE if turn == "o" else curses.A_NORMAL)

        # board
        window.addch(6, 4, board[0][0])
        window.addch(6, 5, curses.ACS_VLINE)
        window.addch(6, 6, board[0][1])
        window.addch(6, 7, curses.ACS_VLINE)
        window.addch(6, 8, board[0][2])

        window.addch(7, 4, curses.ACS_HLINE)
        window.addch(7, 5, "+")
        window.addch(7, 6, curses.ACS_HLINE)
        window.addch(7, 7, "+")
        window.addch(7, 8, curses.ACS_HLINE)

        window.addch(8, 4, board[1][0])
        window.addch(8, 5, curses.ACS_VLINE)
        window.addch(8, 6, board[1][1])
        window.addch(8, 7, curses.ACS_VLINE)
        window.addch(8, 8, board[1][2])

        window.addch(9, 4, curses.ACS_HLINE)
        window.addch(9, 5, "+")
        window.addch(9, 6, curses.ACS_HLINE)
        window.addch(9, 7, "+")
        window.addch(9, 8, curses.ACS_HLINE)

        window.addch(10, 4, board[2][0])
        window.addch(10, 5, curses.ACS_VLINE)
        window.addch(10, 6, board[2][1])
        window.addch(10, 7, curses.ACS_VLINE)
        window.addch(10, 8, board[2][2])


        # make cursor visible
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
                turn = "x" if turn == "o" else "o"
                continue
            case curses.KEY_Q:
                pass

        window.refresh()
    # score screen
    curses.curs_set(0)

wrapper(main)
