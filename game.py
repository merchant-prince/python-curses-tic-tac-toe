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

            case curses.KEY_ENTER | 10: # apparently curses.KEY_ENTER is unreliable. pressing the 'Enter' key yields the keycode 10. using both for a more consistent result
                break

        window.refresh()

    # game screen

    # score screen

wrapper(main)
