"""AI 模块: 提供简单启发式五子棋电脑对手实现。

当前实现 SimpleAI：
- 基于局部连续子长度平方的简单评分函数；
- 同时考虑己方延伸与对手阻断；
- 在最近落子周围生成候选以降低复杂度。
后续可扩展更高级搜索 (Alpha-Beta, MCTS)。
"""
from __future__ import annotations
from typing import Tuple, Optional  # 移除未使用的 List
from .board import Board, Stone

class SimpleAI:
    """极简启发式 AI：
    - 搜索所有空位，评估当前方落子分数。
    - 评分=最大己方连子潜力 + 阻断对方连子潜力（稍低权重）。
    """
    def __init__(self, stone: str):
        """初始化 AI。

        参数:
            stone: AI 使用的棋子颜色 ('B' 或 'W')。
        """
        self.stone = stone
        self.opponent = Stone.WHITE if stone == Stone.BLACK else Stone.BLACK

    def evaluate_point(self, board: Board, r: int, c: int) -> int:
        """评估在 (r,c) 落子后的局部启发式分数。

        评分由四个方向的己方与对方连续数平方加权组成。
        """
        score = 0
        directions = [(1,0),(0,1),(1,1),(1,-1)]
        for dr, dc in directions:
            my_run = self._line_run(board, r, c, dr, dc, self.stone)
            opp_run = self._line_run(board, r, c, dr, dc, self.opponent)
            score += my_run * my_run * 10  # 自身连子优先
            score += opp_run * opp_run * 6  # 阻挡对手
        return score

    def _line_run(self, board: Board, r: int, c: int, dr: int, dc: int, stone: str) -> int:
        """计算假设在 (r,c) 放置后，方向 (dr,dc) 上含该点的连续 stone 数量。"""
        # count contiguous stones including hypothetical placement
        count = 1  # the hypothetical stone
        i = 1
        while board.inside(r+dr*i, c+dc*i) and board.get(r+dr*i, c+dc*i) == stone:
            count += 1; i += 1
        i = 1
        while board.inside(r-dr*i, c-dc*i) and board.get(r-dr*i, c-dc*i) == stone:
            count += 1; i += 1
        return count

    def best_move(self, board: Board) -> Optional[Tuple[int,int]]:
        """返回当前局面下的最佳落点 (r,c)。若为空棋盘返回中心。"""
        best: Optional[Tuple[int,int]] = None
        best_score = -1
        size = board.size
        # 优先在已有棋子的邻近范围搜索，减少计算
        candidates = set()
        for mv in board.move_history[-40:]:  # 最近若干步
            for dr in range(-2,3):
                for dc in range(-2,3):
                    nr, nc = mv.row+dr, mv.col+dc
                    if board.inside(nr, nc) and board.get(nr,nc)==Stone.EMPTY:
                        candidates.add((nr,nc))
        if not candidates:  # 开局
            mid = size//2
            return (mid, mid)
        for r, c in candidates:
            s = self.evaluate_point(board, r, c)
            if s > best_score:
                best_score = s
                best = (r,c)
        return best
