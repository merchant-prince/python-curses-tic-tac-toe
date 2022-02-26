from curses import wrapper
import curses

WIDTH = 13
HEIGHT = 15

def main(window):

    # init
    curses.resizeterm(HEIGHT, WIDTH)
    curses.curs_set(0)
    window.getkey()

    # splash screen
    window.clear()
    window.box()

    window.addstr(6, 2, "tic")
    window.addstr(7, 5, "tac")
    window.addstr(8, 8, "toe")

    window.addstr(HEIGHT - 2, 3, "[enter]", curses.A_BLINK)

    window.refresh()
    window.getkey()


    # choice screen

    # game screen

    # score screen

wrapper(main)
