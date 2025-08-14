from __future__ import annotations
from typing import Optional
from .board import Board, Stone
from . import exceptions as exc

class Game:
    def __init__(self, size: int = 15):
        self.board = Board(size)
        self.current = Stone.BLACK
        self.finished = False
        self._winner: Optional[str] = None

    def switch(self):
        self.current = Stone.WHITE if self.current == Stone.BLACK else Stone.BLACK

    def move(self, r: int, c: int):
        if self.finished:
            raise exc.GameFinished("Game already finished")
        self.board.place(r, c, self.current)
        if self.board.winner():
            self.finished = True
            self._winner = self.current
        else:
            if self.board.is_full():
                self.finished = True
            else:
                self.switch()

    def undo(self) -> bool:
        if not self.board.move_history:
            return False
        mv = self.board.undo()
        if self.finished:
            self.finished = False
            self._winner = None
        if mv and mv.stone == self.current:
            # undo removed a stone of current, so switch back for correct turn
            self.switch()
        return True

    def winner(self) -> Optional[str]:
        return self._winner

    def save(self, path: str):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.board.serialize()+"\n")
            f.write(self.current+"\n")
            f.write((self._winner or "")+"\n")

    @classmethod
    def load(cls, path: str) -> 'Game':
        with open(path, 'r', encoding='utf-8') as f:
            board_data = f.readline().rstrip('\n')
            current = f.readline().strip()
            winner_line = f.readline().strip()
        board = Board.deserialize(board_data)
        g = cls(board.size)
        g.board = board
        g.current = current
        g._winner = winner_line or None
        g.finished = bool(g._winner) or board.is_full()
        return g
