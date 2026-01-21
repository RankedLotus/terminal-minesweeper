import curses
import random
from collections import defaultdict
import heapq

SIZE = 4
EMPTY = 0

def is_solvable(board):
    inversions = 0
    tiles = [x for x in board if x != EMPTY]

    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1

    empty_index = board.index(EMPTY)
    empty_row_from_top = empty_index // SIZE
    blank_row_from_bottom = SIZE - empty_row_from_top  # 1-based

    # For even grid width (4x4)
    return (inversions + blank_row_from_bottom) % 2 == 1



def shuffle_board():
    board = list(range(1, SIZE * SIZE))
    board.append(EMPTY)

    while True:
        random.shuffle(board)
        if is_solvable(board) and not is_solved(board):
            return board


def is_solved(board):
    return board == list(range(1, SIZE * SIZE)) + [EMPTY]


def stringify(board):
    ans = ""

    for i in board:
        ans += str(i) + " "

    return ans


def genPoss(board):
    # identify ind of 0
    ind = -1
    for i in range(16):
        if board[i] == 0:
            ind = 1
            # break <- this should work fine but test w/o first
    x = ind % 4
    y = ind // 4
    answs = []
    # left
    if x > 0:
        myL = board.copy()
        myL[ind] = myL[ind - 1]
        myL[ind - 1] = 0
        answs.append(myL)
    if x < 3:
        myL = board.copy()
        myL[ind] = myL[ind + 1]
        myL[ind + 1] = 0
        answs.append(myL)
    if y > 0:
        myL = board.copy()
        myL[ind] = myL[ind - 4]
        myL[ind - 4] = 0
        answs.append(myL)
    if y < 3:
        myL = board.copy()
        myL[ind] = myL[ind + 4]
        myL[ind + 4] = 0
        answs.append(myL)
    return answs


# THIS SHOULD CRAWL THROUGH ALL PREVIOUS STATES AND MAKE A TREE
def crawler(board, original, parents):
    if board == original:
        return [board]
    else:
        return crawler(parents[board], original, board).append(board)

def astar(board):
    solved = list(range(1, SIZE * SIZE)) + [EMPTY]

    # set up priority queue:
    pq = []
    heapq.heapify(pq)

    heapq.heappush(pq, (heuristic(board), board)) #

    # setting up other data structures
    parent = defaultdict()
    seen = set()
    seen.add(stringify(board))

    # algorithm
    curr = board
    #assumes board is solvable
    while curr != solved:
        curr = heapq.heappop(pq)

        dist = curr[0]
        myL = curr[1]
        strL = stringify(myL)


        # now you have to add the rest of the options to the pq
        for option in genPoss(myL):
            if stringify(option) not in seen:

                seen.add(stringify(option))
                heapq.heappush(pq, (heuristic(option), option))

                parent[stringify(option)] = strL


    # take parent chain of answer out of parent dictionary
    ans = crawler(board=solved, original=board, parents=parent)

    return ans

def draw(stdscr, board):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    start_y = h // 2 - SIZE
    start_x = w // 2 - SIZE * 3

    for i in range(SIZE):
        for j in range(SIZE):
            value = board[i * SIZE + j]
            y = start_y + i * 2
            x = start_x + j * 6

            if value == EMPTY:
                stdscr.addstr(y, x, "     ")
            else:
                stdscr.addstr(y, x, f"[{value:2}]")



    stdscr.addstr(start_y + SIZE * 2 + 1, start_x,
                  "Arrow keys: move | s: shuffle | q: quit")
    stdscr.addstr("\n" + str(heuristic(board)))

    stdscr.addstr("\n" + str(board))

    if is_solved(board):
        stdscr.addstr(start_y - 2, start_x, "Puzzle Solved!")

    stdscr.refresh()


def heuristic(board):
    total = 0

    for index, value in enumerate(board):
        if value == EMPTY:
            continue

        # Current position
        cur_row, cur_col = divmod(index, SIZE)

        # Goal position (value 1 belongs at index 0, etc.)
        goal_index = value - 1
        goal_row, goal_col = divmod(goal_index, SIZE)

        total += abs(cur_row - goal_row) + abs(cur_col - goal_col)

    return total


def move(board, direction):
    idx = board.index(EMPTY)
    r, c = divmod(idx, SIZE)

    drdc = {
        curses.KEY_UP: (-1, 0),
        curses.KEY_DOWN: (1, 0),
        curses.KEY_LEFT: (0, -1),
        curses.KEY_RIGHT: (0, 1),
    }

    if direction not in drdc:
        return

    dr, dc = drdc[direction]
    nr, nc = r + dr, c + dc

    if 0 <= nr < SIZE and 0 <= nc < SIZE:
        nidx = nr * SIZE + nc
        board[idx], board[nidx] = board[nidx], board[idx]


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    board = shuffle_board()

    while True:
        draw(stdscr, board)
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == ord('s'):
            board = shuffle_board()
        elif key == ord('a'):
            pass
        else:
            move(board, key)

    astarpath = astar(board)
    print(astarpath)

    abc = stdscr.getch()
    print(abc)



if __name__ == "__main__":
    curses.wrapper(main)
