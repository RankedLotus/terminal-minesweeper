from enum import Enum
from typing import List, Tuple, Optional
import random

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
    moveset = [Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT]

    def __init__(self):
        pass


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

                        cbscore = Board.score(Board.make_move(cb4, m4))
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

                    cbscore = Board.score(Board.make_move(cb3, m3))
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

                cbscore = Board.score(Board.make_move(cb2, m2))
                if cbscore > bestboard:
                    bestboard = cbscore
                    bestmove = move
        return bestmove


    # @staticmethod
    def next_move(self, currBoard, strat : StratType) -> Move:
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
                cbscore = Board.score(Board.make_move(cb, move))
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

b = Board([
    1, 1, 0, 0,
    2, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0
])

# print(b)
# print("Score:", b.score())
# print("Legal moves:", b.legal_moves())


# imp = ""
# while(imp != "q"):
#     print(b)
#     print("Score:", b.score())
#
#     imp = input("next move?\n")
#     if imp == "w":
#         b = b.make_move(Move.UP)
#     elif imp == "s":
#         b = b.make_move(Move.DOWN)
#     elif imp == "d":
#         b = b.make_move(Move.RIGHT)
#     elif imp == "a":
#         b = b.make_move(Move.LEFT)
#     elif imp == "r":
#         b = b.make_move(Strategy.next_move(currBoard=b, strat=StratType.RAND))
#     elif imp == "t":
#         b = b.make_move(Strategy.next_move(currBoard=b, strat=StratType.SHORTSIGHT))