import curses
import random
from curses import wrapper

GRID_X = 30
GRID_Y = 16
X_SPACER = 2
NUM_MINES = 75

# THIS MIGHT HAVE TO RETURN SOMETHING
def incTile(bigstr, mineset, tile):
    # if the tile isn't a mine
    a = tile[0]
    b = tile[1]
    if (tile not in mineset and
            a >= 0 and
            b >= 0 and
            a < GRID_X and
            b < GRID_Y):
        num = int(ord(bigstr[a + (b * GRID_X)]))
        bigstr[a + (b * GRID_X)] = chr(num + 1)


def genRealBoard(cursorPos):
    mineset = genMines(NUM_MINES, cursorPos)
    bigstr = ['0'] * (GRID_X * GRID_Y)

    for (a, b) in mineset:
        bigstr[a + (b * GRID_X)] = 'X'
        # add numbers
        incTile(bigstr, mineset, (a, b - 1))
        incTile(bigstr, mineset, (a, b + 1))
        incTile(bigstr, mineset, (a + 1, b))
        incTile(bigstr, mineset, (a - 1, b))
        incTile(bigstr, mineset, (a - 1, b - 1))
        incTile(bigstr, mineset, (a + 1, b - 1))
        incTile(bigstr, mineset, (a - 1, b + 1))
        incTile(bigstr, mineset, (a + 1, b + 1))


    return bigstr

def genMines(num: int, cursorPos):
    # make set of all positions and remove chosen position from set
    cmines = set()
    count = 0
    while(count < num):
        rx = random.randint(0, GRID_X - 1)
        ry = random.randint(0, GRID_Y - 1)
        tpair = (rx, ry)

        #check if pair exists, only inc counter if it does
        if tpair not in cmines and tpair != cursorPos:
            cmines.add(tpair)
            count += 1

    return cmines


def drawBoard(win, mines, cleared, realboard, mine_counter, status):
    # colors
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)

    for y in range(GRID_Y):
        for x in range(GRID_X):
            # if mine is marked, draw M
            if mines[x + (y * GRID_X)]:
                win.addstr(y, x * X_SPACER, "M", curses.A_REVERSE)
            # if mine is cleared, draw real board
            elif cleared[x + (y * GRID_X)]:
                val = realboard[x + (y * GRID_X)]
                if val == '0':
                    win.addstr(y, x * X_SPACER, " ")
                elif val == '1':
                    win.addstr(y, x * X_SPACER, "1", curses.color_pair(1))
                elif val == '2':
                    win.addstr(y, x * X_SPACER, "2", curses.color_pair(2))
                elif val == '3':
                    win.addstr(y, x * X_SPACER, "3", curses.color_pair(3))
                elif val == '4':
                    win.addstr(y, x * X_SPACER, "4", curses.color_pair(4))
                elif val == '5':
                    win.addstr(y, x * X_SPACER, "5", curses.color_pair(5))
                elif val == '6':
                    win.addstr(y, x * X_SPACER, "6", curses.color_pair(6))
                elif val == '7':
                    win.addstr(y, x * X_SPACER, "7", curses.color_pair(7))
                elif val == '8':
                    win.addstr(y, x * X_SPACER, "8", curses.color_pair(8))
                else:
                    win.addstr(y, x * X_SPACER, str(val))
            # else, filler
            else:
                win.addstr(y, x * X_SPACER, ". ")

        win.addstr("\n")
    win.addstr("=" * GRID_X * X_SPACER)
    win.addstr("\n")
    win.addstr("GAME STATUS: " + status + "\n")
    win.addstr("Number of mines left: ")
    win.addstr(str(NUM_MINES - mine_counter) + ". \n")
    win.addstr("PRESS [q] TO QUIT GAME, PRESS [r] TO RESET BOARD")
    win.addstr("\nPROJECT MADE BY GABRIEL POMIAN")

def im(realboard, tile):
    ind = tile[0] + (tile[1] * GRID_X)
    if realboard[ind] == 'X':
        return 1
    else:
        return 0


def numMines(realboard, tile): #rb = realboard
    x = tile[0]
    y = tile[1]
    ans = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i != 0 or j != 0:
                ans += im(realboard, (x + i, y + j))
    return ans

def cth(real_board, cleared, tile):
    x = tile[0]
    y = tile[1]
    if x >= 0 and y >= 0 and x < GRID_X and y < GRID_Y:
        ind = x + (y * GRID_X)
        if cleared[ind] == False and real_board[ind] != 'X':
            cleared[ind] = True
            if real_board[x + (y * GRID_X)] == '0':
                clearTile(real_board, cleared, (x, y + 1))
                clearTile(real_board, cleared, (x + 1, y + 1))
                clearTile(real_board, cleared, (x - 1, y + 1))
                clearTile(real_board, cleared, (x + 1, y))
                clearTile(real_board, cleared, (x - 1, y))
                clearTile(real_board, cleared, (x + 1, y - 1))
                clearTile(real_board, cleared, (x, y - 1))
                clearTile(real_board, cleared, (x - 1, y - 1))


def clearTile(real_board, cleared, tile, marked, og):
    x = tile[0]
    y = tile[1]
    if x >= 0 and y >= 0 and x < GRID_X and y < GRID_Y:
        ind = x + (y * GRID_X)
        if cleared[ind] == False and marked[ind] == False:
            cleared[ind] = True
            if real_board[x + (y * GRID_X)] == '0':
                m = marked
                clearTile(real_board, cleared, (x, y + 1), m, False)
                clearTile(real_board, cleared, (x + 1, y + 1), m, False)
                clearTile(real_board, cleared, (x - 1, y + 1), m, False)
                clearTile(real_board, cleared, (x + 1, y), m, False)
                clearTile(real_board, cleared, (x - 1, y), m, False)
                clearTile(real_board, cleared, (x + 1, y - 1), m, False)
                clearTile(real_board, cleared, (x, y - 1), m, False)
                clearTile(real_board, cleared, (x - 1, y - 1), m, False)
        elif og:
            if real_board[ind] in "12345678":
                n_marked = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i != 0 or j != 0:
                            # make sure its within bounds
                            a = x + i
                            b = y + j
                            if a >= 0 and b >= 0 and a < GRID_X and b < GRID_Y:
                                mInd = a + (b * GRID_X)
                                if marked[mInd]:
                                    n_marked += 1

                if n_marked == int(real_board[ind]):
                    #real_board[ind] = 'B'
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i != 0 or j != 0:
                                a = x + i
                                b = y + j
                                if a >= 0 and b >= 0 and a < GRID_X and b < GRID_Y:
                                    ind = a + (b * GRID_X)
                                    clearTile(real_board, cleared, (a, b), marked, False)
                                # clearTile(real_board, cleared, (x + i, y + j), marked, False)

                            #cth(real_board, cleared,(x + i, y + j))
        # PUT CHORDING CODE HERE


def arrowsHandler(key, win, cursorPos):
    dp = (0, 0)
    # MOVING THE CURSOR
    if key == curses.KEY_UP and cursorPos[1] > 0:
        dp = (0, -1)
    elif key == curses.KEY_DOWN and cursorPos[1] < GRID_Y - 1:
        dp = (0, 1)
    elif key == curses.KEY_LEFT and cursorPos[0] > 0:
        dp = (-1 * X_SPACER, 0)
    elif key == curses.KEY_RIGHT and cursorPos[0] < (GRID_X * X_SPACER) - 1:
        dp = (1 * X_SPACER, 0)

    return dp

def refreshWin(win, cursorPos):
    win.clear()
    win.refresh()
    # win.border()
    changeMade = False
    win.move(cursorPos[1], cursorPos[0])

def count_clear(cleared):
    ans = 0
    for tile in cleared:
        if tile:
            ans += 1
    return ans
def main(stdscr):
    status = "PLAYING"
    clear_counter = 0
    mine_counter = 0
    mines = [False] * (GRID_X * GRID_Y)
    cleared = [False] * (GRID_X * GRID_Y)
    realboard = genRealBoard((0, 0))
    isFirstMove = True

    cursorPos = (0, 0)

    stdscr.clear()
    stdscr.refresh()
    win = curses.newwin(GRID_Y + 5, (X_SPACER * GRID_X) + 3, 0, 8)
    win.keypad(True) # makes arrow keys easier to read
    win.nodelay(True) # makes getch not block the program

    win.move(cursorPos[1], cursorPos[0])

    win.clear()
    win.refresh()
    # win.border()

    changeMade = True
    while True:
        # sets the cursor value to the current point
        win.move(cursorPos[1], cursorPos[0])

        #refreshes the screen only if a change is made
        if changeMade:
            refreshWin(win, cursorPos)
            changeMade = False
            clear_counter = count_clear(cleared)
            if clear_counter + NUM_MINES == GRID_Y * GRID_X:
                status = "WON"
            if status == "LOST":
                cleared = [True] * (GRID_X * GRID_Y)
            drawBoard(win, mines, cleared, realboard, mine_counter, status)

        key = win.getch()

        # handling arrow key input
        dp = arrowsHandler(key, win, cursorPos)

        # quitting the game
        if key == ord('q'):
            break

        # restarting the game
        if key == ord('r'):
            status = "PLAYING"
            isFirstMove = True
            mine_counter = 0
            mines = [False] * (GRID_X * GRID_Y)
            cleared = [False] * (GRID_X * GRID_Y)
            changeMade = True


        # marking a mine
        # remember, [0] is x, whcih is scaled; [1] is y which is unscaled
        ind: int = (cursorPos[0] // X_SPACER) + (GRID_X * cursorPos[1])

        if key == ord('m'):
            if not cleared[ind]:
                mines[ind] = not mines[ind]
                if mines[ind]:
                    mine_counter += 1
                else:
                    mine_counter -= 1
                changeMade = True
        # clearing a mine
        if key == ord(' '):
            # losing if mine on not first move
            if realboard[ind] == 'X' and not isFirstMove:
                status = "LOST"

            #if first move and hit mine, move it
            if isFirstMove:
                isFirstMove = False
                realboard = genRealBoard(cursorPos)
                changeMade = True

            # check you're not trying to clear a marked square
            if not mines[ind] and not isFirstMove:
                clearTile(realboard, cleared, (cursorPos[0] // X_SPACER, cursorPos[1]), mines, True)
                changeMade = True

        if status == "PLAYING":
            for i in range(GRID_X * GRID_Y):
                if cleared[i] and (realboard[i] == 'X'):
                    changeMade = True
                    status = "LOST"

        if dp != (0, 0):
            cursorPos = (cursorPos[0] + dp[0], cursorPos[1] + dp[1])
        # end of while loop for game

    # clearing old window and ending game
    win.clear()
    win.refresh()
    stdscr.clear()
    stdscr.refresh()
    stdscr.addstr("Thanks for playing!\ntype a key to exit: ")
    stdscr.getch()


wrapper(main)