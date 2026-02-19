from enum import Enum
from typing import List, Tuple, Optional
import random
import time
import math
from collections import defaultdict

class Move(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class StratType(Enum):
    RAND = "Rand"
    DOWNLEFT = "Downleft"
    SHORTSIGHT = "Shortsight"
    LOOK2 = "Look2"
    LOOK3 = "Look3"
    LOOK4 = "Look4"

class Strategy():
    empty_weight: float
    snake_weight: float
    moveset = [Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT]
    abk_snake = [4**15, 4**14, 4**13, 4**12, 4**8, 4**9, 4**10, 4**11, 4**7, 4**6, 4**5, 4**4, 4**0, 4**1, 4**2, 4**3]


    def __init__(self, ew=1.0, sw=1.0, tw=(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)):
        self.empty_weight = ew
        self.snake_weight = sw
        self.tile_weights = tw


    def heuristic(self, currBoard):
        mSum = 0
        cbd = currBoard.cells
        eti = 0
        for i in range(16):
            if cbd[i] == 0:
                eti += 1
            else:
                # mSum += math.pow(2,cbd[i]) * (16 - i) * (16 - i)
                mSum += self.abk_snake[i] * (2 ** cbd[i])
        return Board.score(currBoard)# mSum#Board.score(currBoard) * self.snake_weight # + eti * eti * self.empty_weight
        # return eti * self.empty_weight + mSum * self.snake_weight
        # return mSum + (eti * eti) * 4096

    def heuristic_test(self, currBoard):
        mSum = 0
        largest = 0
        # sndlargest = 0
        ntiles = 0
        corners = {0, 3, 12, 15}
        cbc = currBoard.cells
        for tile in cbc:
            if tile > largest:
                largest = tile

        for i in range(len(cbc)):
            base_score = math.pow(2, cbc[i]) * (cbc[i] - 1)
            if i <= 3 and largest - i == cbc[i]:
                mSum += math.pow(2, largest) * (largest - 1)
            else:
                mSum += base_score
        #     if tile > 0:
        #         if tile > largest:
        #             largest = tile
        #         ntiles += 1
        #     elif tile > sndlargest and tile != largest:
        #         sndlargest = tile
        #     mSum += tile # math.pow(2, tile)
        # trsum = cbc[0] + cbc[1] + cbc[2] + cbc[3]
        # seq = 0
        # if largest == cbc[0]:
        #     seq += ntiles
        # if sndlargest == cbc[1]:
        #     seq += ntiles
        return mSum

    def custom_depth_look(self, currBoard, depth):
        bestboard = 0
        bestmove = None
        total_best = 0
        poss_moves = Board.legal_moves(currBoard)
        # iterate through the possible moves from your current board state.
        for move in poss_moves:
            cb = Board.copy(currBoard)
            cb = Board.make_move(cb, move)
            cbh = self.heuristic(cb)
            # if you're at the bottom, just compare the 4 you can see from here
            if depth == 1:
                if cbh > bestboard:
                    bestboard = cbh
            # otherwise, keep digging down.
            else:
                (bboard, bmove) = self.custom_depth_look(cb, depth - 1)
                if bboard > bestboard:
                    bestboard = bboard
                    bestmove = move

        return (bestboard, bestmove)

    def four_move_look(self, currBoard):
        bestboard = 0
        bestmove = None
        poss_moves = Board.legal_moves(currBoard)
        # first layer
        for move in poss_moves:
            # copies first one and makes the move
            cb = Board.copy(currBoard)
            cb = Board.make_move(cb, move)
            # second layer possible moves and iterate
            pm2 = Board.legal_moves(cb)
            for m2 in pm2:
                #make move 2
                cb2 = Board.copy(cb)
                cb2 = Board.make_move(cb2, m2)

                pm3 = Board.legal_moves(cb2)
                for m3 in pm3:
                    cb3 = Board.copy(cb2)

                    cb3 = Board.make_move(cb3, m3)
                    pm4 = Board.legal_moves(cb3)
                    for m4 in pm4:
                        cb4 = Board.copy(cb3)

                        cbscore = self.heuristic(Board.make_move(cb4, m4)) #Board.score(Board.make_move(cb4, m4))
                        if cbscore > bestboard:
                            bestboard = cbscore
                            bestmove = move
        return bestmove

    #@staticmethod

    def three_move_look(self, currBoard):
        bestboard = 0
        bestmove = None
        poss_moves = Board.legal_moves(currBoard)
        # first layer
        for move in poss_moves:
            # copies first one and makes the move
            cb = Board.copy(currBoard)
            cb = Board.make_move(cb, move)
            # second layer possible moves and iterate
            pm2 = Board.legal_moves(cb)
            for m2 in pm2:
                #make move 2
                cb2 = Board.copy(cb)
                cb2 = Board.make_move(cb2, m2)

                pm3 = Board.legal_moves(cb2)
                for m3 in pm3:
                    cb3 = Board.copy(cb2)

                    cbscore = self.heuristic(Board.make_move(cb3, m3))# Board.score(Board.make_move(cb3, m3))
                    if cbscore > bestboard:
                        bestboard = cbscore
                        bestmove = move
        return bestmove

    def two_move_look(self, currBoard):
        bestboard = 0
        bestmove = None
        poss_moves = Board.legal_moves(currBoard)
        # first layer
        for move in poss_moves:
            # copies first one and makes the move
            cb = Board.copy(currBoard)
            cb = Board.make_move(cb, move)
            # second layer possible moves and iterate
            pm2 = Board.legal_moves(cb)
            for m2 in pm2:
                cb2 = Board.copy(cb)

                cbscore = self.heuristic(Board.make_move(cb2, m2))# Board.score(Board.make_move(cb2, m2))
                if cbscore > bestboard:
                    bestboard = cbscore
                    bestmove = move
        return bestmove


    # @staticmethod
    def next_move(self, currBoard, strat : StratType) -> Move:
        if True:
            (bboard, bmove) = self.custom_depth_look(currBoard, 3)
            return bmove

        if strat == StratType.RAND:
            poss_moves = Board.legal_moves(currBoard)
            if len(poss_moves) > 0:
                return poss_moves[random.randint(0, len(poss_moves)) - 1]
            else:
                return None

        if strat == StratType.SHORTSIGHT:
            bestboard = 0
            bestmove = None
            poss_moves = Board.legal_moves(currBoard)
            for move in poss_moves:
                cb = Board.copy(currBoard)
                cbscore = self.heuristic(cb)#Board.score(Board.make_move(cb, move))
                if cbscore > bestboard:
                    bestboard = cbscore
                    bestmove = move

            return bestmove

        if strat == StratType.LOOK2:
            return self.two_move_look(currBoard)

        if strat == StratType.LOOK3:
            return self.three_move_look(currBoard)

        if strat == StratType.LOOK4:
            return self.four_move_look(currBoard)


class Board:
    SIZE = 4
    CELLS = 16

    def __init__(self, cells: Optional[List[int]] = None):
        if cells is None:
            self.cells = [0] * self.CELLS
        else:
            if len(cells) != self.CELLS:
                raise ValueError("Board must contain exactly 16 integers")
            self.cells = list(cells)

    # -------------------------
    # Representation utilities
    # -------------------------

    def freeze(self) -> Tuple[int, ...]:
        """Return an immutable representation of the board."""
        return tuple(self.cells)

    @staticmethod
    def unfreeze(state: Tuple[int, ...]) -> "Board":
        """Recreate a Board from a frozen state."""
        return Board(list(state))

    def copy(self) -> "Board":
        return Board(self.cells)

    # -------------------------
    # Scoring
    # -------------------------

    def score(self) -> int:
        """
        Compute the 2048 score assuming all tiles originated as 2s.
        score(2^n) = 2^n * (n - 1)
        """
        total = 0
        for n in self.cells:
            if n > 1:
                total += (2 ** n) * (n - 1)
        return total

    # -------------------------
    # Move logic
    # -------------------------

    def legal_moves(self) -> List[Move]:
        """Return all moves that change the board."""
        moves = []
        for move in Move:
            if self.make_move(move).cells != self.cells:
                moves.append(move)
        return moves

    def nempty(self):
        ans = []

        for i in range(len(self.cells)):
            if self.cells[i] == 0:
                ans.append(i)

        return ans

    def make_move(self, move: Move) -> "Board":
        """Apply a move and return the resulting board."""
        new = self.copy()

        if move == Move.LEFT:
            # has_moved = True
            for r in range(4):
                row = new._get_row(r)
                new._set_row(r, self._merge_line(row))

        elif move == Move.RIGHT:
            # has_moved = True
            for r in range(4):
                row = list(reversed(new._get_row(r)))
                merged = self._merge_line(row)
                new._set_row(r, list(reversed(merged)))

        elif move == Move.UP:
            # has_moved = True
            for c in range(4):
                col = new._get_col(c)
                new._set_col(c, self._merge_line(col))

        elif move == Move.DOWN:
            # has_moved = True
            for c in range(4):
                col = list(reversed(new._get_col(c)))
                merged = self._merge_line(col)
                new._set_col(c, list(reversed(merged)))

        has_moved = False

        if new.cells != self.cells:
            has_moved = True

        if has_moved:
            empty_tiles = new.nempty()
            spot = empty_tiles[random.randint(0, len(empty_tiles) - 1)]
            new.cells[spot] = 1

        return new

    # -------------------------
    # Internal helpers
    # -------------------------

    def _merge_line(self, line: List[int]) -> List[int]:
        """Merge a single row or column."""
        nonzero = [x for x in line if x != 0]
        merged = []
        skip = False

        for i in range(len(nonzero)):
            if skip:
                skip = False
                continue
            if i + 1 < len(nonzero) and nonzero[i] == nonzero[i + 1]:
                merged.append(nonzero[i] + 1)
                skip = True
            else:
                merged.append(nonzero[i])

        return merged + [0] * (4 - len(merged))

    def _get_row(self, r: int) -> List[int]:
        i = r * 4
        return self.cells[i:i + 4]

    def _set_row(self, r: int, row: List[int]):
        i = r * 4
        self.cells[i:i + 4] = row

    def _get_col(self, c: int) -> List[int]:
        return [self.cells[c + 4 * r] for r in range(4)]

    def _set_col(self, c: int, col: List[int]):
        for r in range(4):
            self.cells[c + 4 * r] = col[r]

    # -------------------------
    # Pretty printing (optional)
    # -------------------------

    def __str__(self) -> str:
        rows = []
        for r in range(4):
            row = self._get_row(r)
            rows.append(" ".join(f"{(2**n if n else '.'):>4}" for n in row))
        return "\n".join(rows)

testB = Board([
    1, 1, 0, 0,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0
])

b = testB.copy()

bestScore = 0
bestWeights = (0, 0)
def tryOne(mb, strat):
    nx = strat.next_move(mb, StratType.LOOK3)

    while nx != None:
        mb = Board.make_move(mb, nx)
        nx = strat.next_move(mb, StratType.LOOK3)

    print("board done")
    return mb

# print(b)
# print("Score:", b.score())
# print("Legal moves:", b.legal_moves())
# strB = Strategy()
#
# next = strB.next_move(b, StratType.LOOK3)
#
# start = time.perf_counter()

# while next != None:
#     b = Board.make_move(b, next)
#     next = strB.next_move(b, StratType.LOOK3)
#
# end = time.perf_counter()
#
# print(b)
# print(f"Score: {b.score()}")

# print(f"elapsed time: {end - start}")





#
# f1 = open("score_reg.txt", "a")
#
# for i in range(5): #number of weight changes
#     avgscore = 0
#     # ew = random.random() * 10 * random.random()
#     # sw = random.random() * 10 * random.random() * 10
#     # tile_weights = []
#     # for rr in range(16):
#     #     tile_weights.append(random.random() * 50)
#     # tw = tuple(tile_weights)
#     tw = (16, 12, 8, 4,
#           12, 8, 4, 3,
#           8, 4, 3, 2,
#           4, 3, 2, 1)
#     print(f"the tile weights: {tw}")
#     ew = 1
#     sw = 1
#
#     strB = Strategy(ew, sw, tw)
#     for j in range(10): #number of trials per weight
#         newB = testB.copy()
#         endB = tryOne(newB, strB)
#         avgscore += Board.score(endB) / 5
#         f1.write(str(Board.score(endB)) + "\n")
#
#     print(avgscore)
#     if avgscore > bestScore:
#         bestScore = avgscore
#         bestWeights = (ew, sw)
#         print(bestWeights)
#
# # print(f"Best weight: {bestWeights}")
# # print(f"Best score: {bestScore}")
# f1.close()
