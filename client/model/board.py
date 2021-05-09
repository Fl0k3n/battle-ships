from utils.color import Color
from model.cell import Cell
from model.pawn import Pawn
from typing import List, Tuple, Dict


class Board:
    def __init__(self, n: int = 8, pawn_rows: int = 3):
        self.n = n
        self.pawn_rows = pawn_rows
        self.board = []
        self.white_pawns = {}
        self.black_pawns = {}

        self.pawns = {
            Color.WHITE: self.white_pawns,
            Color.BLACK: self.black_pawns
        }

        self._init_board_layout()
        self.valid_moves = {}

    def _init_board_layout(self) -> None:
        for i in range(self.n):
            row = []
            for j in range(self.n):
                color = Color.BLACK if j % 2 == 0 else Color.WHITE
                if i % 2 == 1:
                    color = Color.reverse(color)

                cell = Cell(i, j, color)
                row.append(cell)

                if (i < self.pawn_rows or i > self.n - self.pawn_rows - 1) and color == Color.BLACK:
                    pawn_color = Color.BLACK if i < self.pawn_rows else Color.WHITE
                    pawn = Pawn(i, j, pawn_color)
                    self.pawns[pawn_color][(i, j)] = pawn

                    cell.place_pawn(pawn)

            self.board.append(row)

    def get_cell(self, i: int, j: int) -> Cell:
        return self.board[i][j]

    def get_board(self) -> List[List[Cell]]:
        return self.board

    def get_n_fields(self) -> int:
        return self.n

    def get_valid_moves(self) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
        return self.valid_moves

    def get_valid_moves_from(self, cell: Cell) -> List[Tuple[int, int]]:
        moves = self.valid_moves.get(cell.get_position())
        return moves if moves is not None else []

    def update_valid_moves(self, turn: Color) -> None:
        valid_moves = []
        best_moves_len = 0

        for (i, j), pawn in self.pawns[turn].items():
            paths = self._get_max_consec(i, j, pawn)
            if len(paths) > 0:
                lp0 = len(paths[0])
                if lp0 == best_moves_len:
                    valid_moves.extend(paths)
                elif lp0 > best_moves_len:
                    best_moves_len = lp0
                    valid_moves = paths

        if best_moves_len == 0:
            # handle free positions separately
            for (i, j), pawn in self.pawns[turn].items():
                for n_i, n_j in self._get_neighs(i, j):
                    if not self.board[n_i][n_j].has_pawn():
                        valid_moves.append([(i, j), (n_i, n_j)])

        self.valid_moves = {all_[0]: [] for all_ in valid_moves}
        for all_ in valid_moves:
            self.valid_moves[all_[0]].extend(all_[1:])

    def _get_neighs(self, i: int, j: int) -> List[Tuple[int, int]]:
        res = []
        for di in (-1, 1):
            for dj in (-1, 1):
                n_i = i + di
                n_j = j + dj
                if 0 <= n_i < self.n and 0 <= n_j < self.n:
                    res.append((n_i, n_j))
        return res

    def _can_jump(self, after_jump_i, after_jump_j) -> bool:
        return 0 <= after_jump_i < self.n and 0 <= after_jump_j < self.n \
            and not self.board[after_jump_i][after_jump_j].has_pawn()

    def _get_max_consec(self, i, j, pawn: Pawn) -> List[List[Tuple[int, int]]]:
        changes = []
        paths = []

        def traverse(cur_i, cur_j, last_i, last_j, color):
            paths = [[(cur_i, cur_j)]]

            for n_i, n_j in self._get_neighs(cur_i, cur_j):
                if last_i == n_i and last_j == n_j:
                    continue
                if self.board[n_i][n_j].get_color() == Color.reverse(color):
                    delta_i = n_i - cur_i
                    delta_j = n_j - cur_j

                    new_i = n_i + delta_i
                    new_j = n_j + delta_j
                    if self._can_jump(new_i, new_j):
                        changes.append(self.board[n_i][n_j].remove_pawn())

                        succ_paths = traverse(new_i, new_j, n_i, n_j, color)
                        paths.extend([[(cur_i, cur_j)].extend(succ_path)
                                     for succ_path in succ_paths])

                        pawn = changes.pop()
                        self.board[n_i][n_j].place_pawn(pawn)

            return paths

        traverse(i, j, -1, -1, pawn.get_color())

        if len(paths) == 0:
            return []

        best_len = len(max(*paths, key=lambda x: len(x)))

        return [path for path in paths if len(path) == best_len]
