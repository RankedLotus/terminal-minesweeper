import curses
import random
from collections import defaultdict
import heapq
from math import inf

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
    return tuple(board)

    ans = ""

    for i in board:
        ans += str(i) + " "

    return ans


def genPoss(board):
    # identify ind of 0
    ind = -1
    for i in range(16):
        if board[i] == 0:
            ind = i
            # break <- this should work fine but test w/o first
    x = ind % 4
    y = ind // 4
    # print("ind: " + str(ind))
    # print("x: " + str(x))
    # print("y: " + str(y))
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
    ans = []
    cb = board
    while(cb != original):
        ans.append(cb)
        cb = parents[cb]
    ans.append(original)
    ans.reverse()
    return ans


# def bstar(board):
#     solved = list(range(1, SIZE * SIZE)) + [EMPTY]
#
#     # set up priority queue:
#     pq = []
#     heapq.heapify(pq)
#
#     heapq.heappush(pq, (heuristic(board), board, 0))
#
#     # setting up other data structures
#     parent = defaultdict()
#     seen = set()
#     # seen.add(stringify(board))
#     dists = defaultdict(lambda: inf)
#     dists[stringify(board)] = 0
#
#     #assumes board is solvable
#     while pq:
#         curr = heapq.heappop(pq)
#
#         totH = curr[0]
#         myL = curr[1]
#         dist = curr[2]
#
#         strL = stringify(myL)
#
#         if curr[1] == solved:
#             break
#
#         seen.add(strL)
#
#         # now you have to add the rest of the options to the pq
#         for option in genPoss(myL):
#             stropt = stringify(option)
#             cdist = dists[strL] + 1
#
#             if cdist < dists[stropt]:
#                 parent[stropt] = strL
#                 dists[stropt] = cdist
#
#                 heapq.heappush(pq, (cdist + heuristic(option), option, cdist))
#             #
#             # if stropt not in seen and dist + 1 < dists[stropt]:
#             #     dists[stropt] = dist + 1
#             #     heapq.heappush(pq, (heuristic(option) + dist + 1, option, dist + 1))
#             #
#             #     parent[stropt] = strL
#
#     # take parent chain of answer out of parent dictionary
#     ans = crawler(board=stringify(solved), original=stringify(board), parents=parent)
#
#     return ans


def bstar(board):
    start = tuple(board)
    goal = tuple(list(range(1, SIZE * SIZE)) + [EMPTY])

    # Priority queue entries: (f = g + h, g, state)
    pq = []
    heapq.heappush(pq, (heuristic(start), 0, start))

    came_from = {}
    g_score = {start: 0}
    closed = set()

    while pq:
        f, g, current = heapq.heappop(pq)

        if current in closed:
            continue
        closed.add(current)

        if current == goal:
            break

        # Expand neighbors
        for nxt in genPoss(list(current)):
            nxt = tuple(nxt)
            tentative_g = g + 1

            if nxt in closed:
                continue

            if tentative_g < g_score.get(nxt, inf):
                came_from[nxt] = current
                g_score[nxt] = tentative_g
                heapq.heappush(
                    pq,
                    (tentative_g + heuristic(nxt), tentative_g, nxt)
                )

    # Reconstruct path
    path = []
    cur = goal
    while cur != start:
        path.append(list(cur))
        cur = came_from[cur]
    path.append(list(start))
    path.reverse()

    return path

def astarC(board):
    solved = list(range(1, SIZE * SIZE)) + [EMPTY]

    pq = []
    heapq.heapify(pq)
    heapq.heappush(pq, (0, board))

    parent = defaultdict()
    # distances = defaultdict(lambda: 1000 * 1000)
    # distances[stringify(board)] = 0

    curr = board

    done = set()

    while pq:
        dist, curr = heapq.heappop(pq)

        if curr == solved:
            break

        done.add(stringify(curr))

        for option in genPoss(board):
            if stringify(option) not in done:
                print(option)
                print("\n")
                heapq.heappush(pq, (dist + 1, option))
                parent[stringify(option)] = stringify(curr)

    # take parent chain of answer out of parent dictionary
    #ans = crawler(board=stringify(solved), original=stringify(board), parents=parent)

    return parent


def astarB(board):
    solved = list(range(1, SIZE * SIZE)) + [EMPTY]

    pq = []
    heapq.heapify(pq)
    heapq.heappush(pq, (heuristic(board), heuristic(board), 0, board)) # distance here is 0

    parent = defaultdict()
    distances = defaultdict(lambda: 1000 * 1000)

    curr = board

    done = set()

    while pq:
        cost, h, dist, curr = heapq.heappop(pq)
        # break if done
        if curr == solved:
            break

        done.add(stringify(curr))

        for option in genPoss(curr):
            if option not in done:
                currD = dist + 1

                if currD < distances[stringify(option)]:
                    distances[stringify(option)] = currD
                    h = heuristic(option)
                    heapq.heappush(pq, (h + currD), h, currD, option)

    # take parent chain of answer out of parent dictionary
    ans = crawler(board=stringify(solved), original=stringify(board), parents=parent)

    return ans

def astar(board):
    solved = list(range(1, SIZE * SIZE)) + [EMPTY]

    # set up priority queue:
    pq = []
    heapq.heapify(pq)
    heapq.heappush(pq, (heuristic(board), board)) #

    # setting up other data structures
    parent = defaultdict()
    distances = defaultdict(lambda: 1000 * 1000)

    seen = set()
    seen.add(stringify(board))

    distances[stringify(board)] = 0

    # algorithm
    curr = board

    #assumes board is solvable

    while curr[1] != solved and pq:
        curr = heapq.heappop(pq)

        currH = curr[0]
        myL = curr[1]
        strL = stringify(myL)
        # print(strL + ", " + str(dist))

        # now you have to add the rest of the options to the pq
        for option in genPoss(myL):
            if True: #stringify(option) not in seen or distances[strL] + 1 < distances[stringify(option)]:

                dist = distances[strL] + 1
                if (stringify(option) not in seen) or (dist < distances[stringify(option)]):
                    distances[stringify(option)] = dist
                    heapq.heappush(pq, (heuristic(option) + distances[stringify(option)], option))
                    parent[stringify(option)] = strL
                    seen.add(stringify(option))

                print(dist)


    # take parent chain of answer out of parent dictionary
    ans = crawler(board=stringify(solved), original=stringify(board), parents=parent)

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

def greedybfs(board):
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

    numits = 0

    #assumes board is solvable
    while curr[1] != solved and pq:
        # print(f"pq len: {len(pq)}")
        numits += 1
        curr = heapq.heappop(pq)

        dist = curr[0]
        myL = curr[1]
        strL = stringify(myL)
        # print(strL + ", " + str(dist))


        # now you have to add the rest of the options to the pq
        for option in genPoss(myL):
            if stringify(option) not in seen:

                seen.add(stringify(option))
                heapq.heappush(pq, (heuristic(option), option))

                parent[stringify(option)] = strL


    # take parent chain of answer out of parent dictionary
    ans = crawler(board=stringify(solved), original=stringify(board), parents=parent)
    return ans # (ans, numits)

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

    crawling = False

    board = shuffle_board()

    while True:
        draw(stdscr, board)
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == ord('s'):
            board = shuffle_board()
        elif key == ord('a'):
            crawling = True
            break
        else:
            move(board, key)

    astarpath = []
    crawlind = 0
    if crawling:
        astarpath = greedybfs(board)

    while crawling:
        board = astarpath[crawlind]
        # btemp = astarpath[crawlind].split()
        # for i in range(16):
        #     board[i] = int(btemp[i])

        draw(stdscr, board)
        key = stdscr.getch()

        if key == curses.KEY_LEFT:
            crawlind = max(0, crawlind - 1)
        elif key == curses.KEY_RIGHT:
            crawlind = min(crawlind + 1, len(astarpath) - 1)
        elif key == ord('q'):
            crawling = False
        else:
            pass


debug = False

if __name__ == "__main__":
    if debug:
        counter : float = 0
        mi = inf
        ma = 0
        for i in range(500):
            board = shuffle_board()
            b, nits = greedybfs(board)
            counter += nits / 500
            mi = min(mi, nits)
            ma = max(ma, nits)
        print(counter)
        print(f"min: {mi}")
        print(f"max: {ma}")
    else:
        curses.wrapper(main)

#SOME PRIOR TESTING STUFF:
# board = shuffle_board() # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 13, 14, 15]# shuffle_board()
# print(board)
# print("options for start: ")
# options = genPoss(board)
# for o in options:
#     print(o)
# print("a* demo: \n")
# b = bstar(board)
# print(b)

