import curses
import random
from curses import wrapper

GRID_X = 30
GRID_Y = 16

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


def genRealBoard():
    mineset = genMines(75)
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

def genMines(num: int):
    # make set of all positions and remove chosen position from set
    cmines = set()
    count = 0
    while(count < num):
        rx = random.randint(0, GRID_X - 1)
        ry = random.randint(0, GRID_Y - 1)
        tpair = (rx, ry)

        #check if pair exists, only inc counter if it does
        if tpair not in cmines:
            cmines.add(tpair)
            count += 1

    return cmines


def drawBoard(win, mines, cleared, realboard):

    for y in range(GRID_Y):
        for x in range(GRID_X):
            # if mine is marked, draw M
            if mines[x + (y * GRID_X)]:
                win.addstr(y, x, "M ")
            # if mine is cleared, draw real board
            elif cleared[x + (y * GRID_X)]:
                val = realboard[x + (y * GRID_X)]
                if val == '0':
                    win.addstr(y, x, " ")
                else:
                    win.addstr(y, x, str(val) + " ")
            # else, filler
            else:
                win.addstr(y, x, ". ")

        win.addstr("\n")
    win.addstr("PRESS 'q' TO QUIT GAME\nPROJECT MADE BY GABRIEL POMIAN")

def clearTile(real_board, cleared, tile):
    x = tile[0]
    y = tile[1]
    if x >= 0 and y >= 0 and x < GRID_X and y < GRID_Y:
        ind = x + (y * GRID_X)
        if cleared[ind] == False:
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



def main(stdscr):
    mines = [False] * (GRID_X * GRID_Y)
    cleared = [False] * (GRID_X * GRID_Y)
    realboard = genRealBoard()

    cursorPos = (10, 10)

    stdscr.clear()
    stdscr.refresh()
    win = curses.newwin(GRID_Y + 2, GRID_X + 5, 0, 8)
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
            win.clear()
            win.refresh()
            # win.border()
            changeMade = False
            drawBoard(win, mines, cleared, realboard)
            win.move(cursorPos[1], cursorPos[0])


        # breaking out of loop

        dp = (0, 0)
        key = win.getch()
        # MOVING THE CURSOR
        if key == curses.KEY_UP and cursorPos[1] > 0:
            dp = (0, -1)
        elif key == curses.KEY_DOWN and cursorPos[1] < GRID_Y - 1:
            dp = (0, 1)
        elif key == curses.KEY_LEFT and cursorPos[0] > 0:
            dp = (-1, 0)
        elif key == curses.KEY_RIGHT and cursorPos[0] < GRID_X - 1:
            dp = (1, 0)
        # quitting the game
        if key == ord('q'):
            break
        # marking a mine
        if key == ord('m'):
            ind: int = cursorPos[0] + (GRID_X * cursorPos[1])
            mines[ind] = not mines[ind]
            changeMade = True
        # clearing a mine
        if key == ord(' '):
            ind: int = cursorPos[0] + (GRID_X * cursorPos[1])
            # check you're not trying to clear a marked square
            if not mines[ind]:
                clearTile(realboard, cleared, cursorPos)
                changeMade = True

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