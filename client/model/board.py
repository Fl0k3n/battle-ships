from utils.color import Color
from model.cell import Cell
from model.pawn import Pawn
from typing import List, Tuple, Dict


class Board:
    def __init__(self, n: int = 8, pawn_rows: int = 3):
        self.n = n
        self.pawn_rows = pawn_rows
        self.board = []
        self.white_pawns = {}  # (i, j) -> Pawn[color=White]
        self.black_pawns = {}  # (i, j) -> Pawn[color=Black]

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

    def get_valid_moves(self) -> Dict[Cell, List[List[Cell]]]:
        return self.valid_moves

    def get_valid_moves_from(self, cell: Cell) -> List[List[Cell]]:
        moves = self.valid_moves.get(cell)
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

        self.valid_moves = {self.get_cell(
            *all_[0]): [] for all_ in valid_moves}

        for all_ in valid_moves:
            rest_cells = [self.get_cell(*pos) for pos in all_[1:]]
            self.valid_moves[self.get_cell(*all_[0])].append(rest_cells)

    def _get_neighs(self, i: int, j: int) -> List[Tuple[int, int]]:
        res = []
        for di in (-1, 1):
            for dj in (-1, 1):
                n_i = i + di
                n_j = j + dj
                if 0 <= n_i < self.n and 0 <= n_j < self.n:
                    res.append((n_i, n_j))
        return res

    def _can_jump(self, after_jump_i: int, after_jump_j: int) -> bool:
        return 0 <= after_jump_i < self.n and 0 <= after_jump_j < self.n \
            and not self.board[after_jump_i][after_jump_j].has_pawn()

    def _get_max_consec(self, i: int, j: int, pawn: Pawn) -> List[List[Tuple[int, int]]]:
        """Gets paths with maximum score starting from cell(i, j) and beating enemy pawn in
           every move.
        Returns:
            List[List[Tuple[int, int]]]: each list is a valid beating path of the same length
        """
        changes = []
        color = pawn.get_color()

        def traverse(cur_i, cur_j, last_i, last_j):
            paths = [[(cur_i, cur_j)]]

            for n_i, n_j in self._get_neighs(cur_i, cur_j):
                if last_i == n_i and last_j == n_j:
                    continue

                cell = self.board[n_i][n_j]
                if cell.has_pawn() and cell.get_pawn().get_color() == Color.reverse(color):
                    delta_i = n_i - cur_i
                    delta_j = n_j - cur_j

                    new_i = n_i + delta_i
                    new_j = n_j + delta_j

                    if self._can_jump(new_i, new_j):
                        changes.append(self.board[n_i][n_j].remove_pawn())

                        succ_paths = traverse(new_i, new_j, n_i, n_j)
                        for succ_path in succ_paths:
                            tmp = [(cur_i, cur_j)]
                            tmp.extend(succ_path)
                            paths.append(tmp)

                        pawn = changes.pop()
                        self.board[n_i][n_j].place_pawn(pawn)

            return paths

        paths = traverse(i, j, -1, -1)

        if len(paths) == 0:
            return []

        best_len = len(max(*paths, key=lambda x: len(x)))

        return [path for path in paths if len(path) == best_len]

    def _get_intermediate_cell(self, start: Cell, end: Cell) -> Cell:
        old_i, old_j = start.get_position()
        new_i, new_j = end.get_position()

        di, dj = new_i - old_i, new_j - old_j
        if abs(di) < 2:
            return None

        return self.get_cell(old_i + di // 2, old_j + dj // 2)

    def move(self, from_: Cell, to_: Cell) -> Cell:
        """Moves pawn from one cell to another, removes beaten pawn if one exists,
            updates valid paths.
        Returns:
            Cell: Cell of beaten pawn if one was beaten, else None
        """
        beaten_cell = self._get_intermediate_cell(from_, to_)

        pawn = from_.remove_pawn()
        self.pawns[pawn.get_color()].pop(pawn.get_position())

        if beaten_cell is not None:
            beaten_pawn = beaten_cell.remove_pawn()
            self.pawns[beaten_pawn.get_color()].pop(beaten_pawn.get_position())

        pawn.move(*to_.get_position())
        to_.place_pawn(pawn)
        self.pawns[pawn.get_color()][pawn.get_position()] = pawn

        old_moves = self.get_valid_moves_from(from_)
        choosen_paths = [path[1:]
                         for path in old_moves if path[0] == to_ and len(path) > 1]
        self.valid_moves = {
            to_: choosen_paths
        }

        return beaten_cell
