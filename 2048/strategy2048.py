from enum import Enum
from board2048 import Board
import math

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

    # @staticmethod
    def next_move(self, currBoard, strat : StratType) -> Move:

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
            (bboard, bmove) = self.custom_depth_look(currBoard, 2)
            return bmove

        if strat == StratType.LOOK3:
            (bboard, bmove) = self.custom_depth_look(currBoard, 3)
            return bmove

        if strat == StratType.LOOK4:
            (bboard, bmove) = self.custom_depth_look(currBoard, 4)
            return bmove