import curses
import random

SIZE = 4
CELL_WIDTH = 6
CELL_HEIGHT = 3


def init_board():
    board = [[0] * SIZE for _ in range(SIZE)]
    add_tile(board)
    add_tile(board)
    return board


def add_tile(board):
    empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        board[r][c] = 4 if random.random() < 0.1 else 2


def compress(row):
    new_row = [x for x in row if x != 0]
    return new_row + [0] * (SIZE - len(new_row))


def merge(row):
    score = 0
    for i in range(SIZE - 1):
        if row[i] != 0 and row[i] == row[i + 1]:
            row[i] *= 2
            score += row[i]
            row[i + 1] = 0
    return row, score


def move_left(board):
    moved = False
    score = 0
    new_board = []

    for row in board:
        compressed = compress(row)
        merged, gained = merge(compressed)
        final = compress(merged)
        if final != row:
            moved = True
        new_board.append(final)
        score += gained

    return new_board, moved, score


def move_right(board):
    reversed_board = [row[::-1] for row in board]
    new_board, moved, score = move_left(reversed_board)
    return [row[::-1] for row in new_board], moved, score


def transpose(board):
    return [list(row) for row in zip(*board)]


def move_up(board):
    t = transpose(board)
    new, moved, score = move_left(t)
    return transpose(new), moved, score


def move_down(board):
    t = transpose(board)
    new, moved, score = move_right(t)
    return transpose(new), moved, score


def has_moves(board):
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                return True
            if c < SIZE - 1 and board[r][c] == board[r][c + 1]:
                return True
            if r < SIZE - 1 and board[r][c] == board[r + 1][c]:
                return True
    return False


def draw_grid(stdscr, start_y, start_x):
    height = SIZE * CELL_HEIGHT
    width = SIZE * CELL_WIDTH

    for y in range(height + 1):
        for x in range(width + 1):
            if y % CELL_HEIGHT == 0 and x % CELL_WIDTH == 0:
                stdscr.addch(start_y + y, start_x + x, curses.ACS_PLUS)
            elif y % CELL_HEIGHT == 0:
                stdscr.addch(start_y + y, start_x + x, curses.ACS_HLINE)
            elif x % CELL_WIDTH == 0:
                stdscr.addch(start_y + y, start_x + x, curses.ACS_VLINE)


def draw(stdscr, board, score):
    stdscr.clear()
    stdscr.addstr(0, 0, f"2048    Score: {score}")
    stdscr.addstr(1, 0, "Arrow keys to move | Q to quit")

    start_y = 3
    start_x = 2

    draw_grid(stdscr, start_y, start_x)

    for r in range(SIZE):
        for c in range(SIZE):
            value = board[r][c]
            if value != 0:
                y = start_y + r * CELL_HEIGHT + CELL_HEIGHT // 2
                x = start_x + c * CELL_WIDTH + CELL_WIDTH // 2 - len(str(value)) // 2
                stdscr.addstr(y, x, str(value))

    stdscr.refresh()


def game(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    solve_mode = "none"

    board = init_board()
    score = 0

    while True:
        draw(stdscr, board, score)

        if not has_moves(board):
            stdscr.addstr(3 + SIZE * CELL_HEIGHT + 1, 0,
                          "Game Over! Press Q to quit.")
            stdscr.refresh()

        key = stdscr.getch()

        mm = "none" # my move

        if key in (ord('q'), ord('Q')):
            break
        elif key in (ord('r'), ord('R')):
            solve_mode = "random"
        elif key == curses.KEY_LEFT:
            mm = "ml"
            # board, moved, gained = move_left(board)
        elif key == curses.KEY_RIGHT:
            mm = "mr"
            # board, moved, gained = move_right(board)
        elif key == curses.KEY_UP:
            mm = "mu"
            # board, moved, gained = move_up(board)
        elif key == curses.KEY_DOWN:
            mm = "md"
            # board, moved, gained = move_down(board)
        else:
            pass

        moves = ["ml", "mr", "mu", "md"]
        if solve_mode == "random":
            mm = moves[random.randint(0, 3)]

        if mm == "ml":
            board, moved, gained = move_left(board)
        elif mm == "mr":
            board, moved, gained = move_right(board)
        elif mm == "mu":
            board, moved, gained = move_up(board)
        elif mm == "md":
            board, moved, gained = move_down(board)

        if moved:
            add_tile(board)
            score += gained


if __name__ == "__main__":
    curses.wrapper(game)
