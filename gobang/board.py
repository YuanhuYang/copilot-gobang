from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Iterable, Tuple

class Stone:
    """棋子类型常量。

    使用单字符表示:
    - "." 空位
    - "B" 黑子 (先手)
    - "W" 白子 (后手)
    """
    EMPTY = "."
    BLACK = "B"
    WHITE = "W"

@dataclass(frozen=True)
class Move:
    """单步落子记录。

    属性:
        row: 行索引 (0 基)
        col: 列索引 (0 基)
        stone: 棋子颜色 ('B' 或 'W')
    """
    row: int
    col: int
    stone: str  # 'B' or 'W'

class Board:
    """棋盘与状态管理。

    维护二维网格、落子历史、最后一步等信息；提供落子、悔棋、胜负检测、序列化等功能。
    """
    def __init__(self, size: int = 15):
        if size < 5:
            raise ValueError("Board size must be >= 5")
        self.size = size
        self.grid: List[List[str]] = [[Stone.EMPTY for _ in range(size)] for _ in range(size)]
        self.last_move: Optional[Move] = None
        self.move_history: List[Move] = []

    def inside(self, r: int, c: int) -> bool:
        return 0 <= r < self.size and 0 <= c < self.size

    def get(self, r: int, c: int) -> str:
        if not self.inside(r, c):
            raise IndexError("Position out of bounds")
        return self.grid[r][c]

    def place(self, r: int, c: int, stone: str) -> None:
        if stone not in (Stone.BLACK, Stone.WHITE):
            raise ValueError("Invalid stone")
        if not self.inside(r, c):
            raise ValueError("Move out of board")
        if self.grid[r][c] != Stone.EMPTY:
            raise ValueError("Cell already occupied")
        self.grid[r][c] = stone
        mv = Move(r, c, stone)
        self.last_move = mv
        self.move_history.append(mv)

    def undo(self) -> Optional[Move]:
        if not self.move_history:
            return None
        mv = self.move_history.pop()
        self.grid[mv.row][mv.col] = Stone.EMPTY
        self.last_move = self.move_history[-1] if self.move_history else None
        return mv

    def iter_lines(self, r: int, c: int, dr: int, dc: int) -> Iterable[Tuple[int,int]]:
        rr, cc = r, c
        while self.inside(rr, cc):
            yield rr, cc
            rr += dr
            cc += dc

    def check_five(self, r: int, c: int) -> bool:
        stone = self.get(r, c)
        if stone == Stone.EMPTY:
            return False
        directions = [(1,0),(0,1),(1,1),(1,-1)]
        for dr, dc in directions:
            count = 1
            # forward
            i = 1
            while self.inside(r+dr*i, c+dc*i) and self.get(r+dr*i, c+dc*i) == stone:
                count += 1; i += 1
            # backward
            i = 1
            while self.inside(r-dr*i, c-dc*i) and self.get(r-dr*i, c-dc*i) == stone:
                count += 1; i += 1
            if count >= 5:
                return True
        return False

    def winner(self) -> Optional[str]:
        if not self.last_move:
            return None
        if self.check_five(self.last_move.row, self.last_move.col):
            return self.last_move.stone
        return None

    def is_full(self) -> bool:
        return all(cell != Stone.EMPTY for row in self.grid for cell in row)

    def to_string(self) -> str:
        header = "   " + " ".join(f"{i:2d}" for i in range(self.size))
        rows = []
        for i, row in enumerate(self.grid):
            rows.append(f"{i:2d} " + "  ".join(row))
        return header + "\n" + "\n".join(rows)

    def serialize(self) -> str:
        moves = ";".join(f"{m.row},{m.col},{m.stone}" for m in self.move_history)
        return f"{self.size}|{moves}"

    @classmethod
    def deserialize(cls, data: str) -> 'Board':
        size_str, moves_str = data.split('|', 1)
        board = cls(int(size_str))
        if moves_str:
            for token in moves_str.split(';'):
                if not token:
                    continue
                r, c, s = token.split(',')
                board.place(int(r), int(c), s)
        return board
