import curses
from clean2048 import Board, Move, Strategy, StratType
import time

CELL_W = 6
TICK = 0.01  # redraw / autoplay speed


def draw_board(stdscr, board: Board, autoplay):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    title = "2048 — WASD move | r=random | t=shortsight | q=quit"
    stdscr.addstr(1, (w - len(title)) // 2, title)

    status = f"Score: {board.score()}   Mode: {autoplay or 'Manual'}"
    stdscr.addstr(3, (w - len(status)) // 2, status)

    top = 5
    left = (w - CELL_W * 4) // 2

    for r in range(4):
        for c in range(4):
            v = board.cells[r * 4 + c]
            text = "." if v == 0 else str(2 ** v)
            x = left + c * CELL_W
            y = top + r * 2
            stdscr.addstr(y, x, f"{text:^{CELL_W}}")

    if not board.legal_moves():
        msg = "GAME OVER"
        stdscr.addstr(top + 9, (w - len(msg)) // 2, msg, curses.A_BOLD)

    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(0)

    stratBook = Strategy()

    board = Board([1, 0, 0, 0,
                   0, 0, 0, 0,
                   0, 0, 0, 0,
                   0, 0, 0, 0])
    board = board.make_move(Move.LEFT)
    board = board.make_move(Move.LEFT)

    autoplay = None
    last_tick = time.time()

    keymap = {
        ord('w'): Move.UP,
        ord('s'): Move.DOWN,
        ord('a'): Move.LEFT,
        ord('d'): Move.RIGHT,
    }

    while True:
        now = time.time()
        ch = stdscr.getch()

        if ch == ord('q'):
            break

        elif ch == ord('r'):
            autoplay = StratType.RAND

        elif ch == ord('t'):
            autoplay = StratType.SHORTSIGHT

        elif ch == ord('2'):
            autoplay = StratType.LOOK2

        elif ch == ord('3'):
            autoplay = StratType.LOOK3

        elif ch == ord('4'):
            autoplay = StratType.LOOK4

        elif ch in keymap:
            autoplay = None
            board = board.make_move(keymap[ch])

        if autoplay and now - last_tick > TICK:
            mv = Strategy.next_move(stratBook, board, autoplay)
            if mv:
                board = board.make_move(mv)
            last_tick = now

        draw_board(stdscr, board, autoplay)
        time.sleep(0.01)


if __name__ == "__main__":
    curses.wrapper(main)