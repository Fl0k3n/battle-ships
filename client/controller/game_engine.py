from model.board import Board
from model.cell import Cell
from view.board_view import BoardView
from view.cell_view import CellView
from view.game_window import GameWindow
from utils.color import Color
from model.player import Player


class GameEngine:
    def __init__(self, game_window: GameWindow):
        self.p1 = Player('kntp1')
        self.p2 = Player('kntp2')

        self.p1.join_game(Color.WHITE)
        self.p2.join_game(Color.BLACK)

        self.board = Board()
        self.game_window = game_window
        self.board_view = self.game_window.draw_board(self.board)

        self.turn = Color.WHITE

        self.board.update_valid_moves(self.turn)
        for move_list in self.board.get_valid_moves().values():
            print([str(cell) for ml in move_list for cell in ml])

    def next_round(self):
        self.turn = Color.reverse(self.turn)
        self.board.update_valid_moves(self.turn)
        # for move_list in self.board.get_valid_moves().values():
        #     print([str(cell) for ml in move_list for cell in ml])

    def get_board_view(self) -> BoardView:
        return self.board_view

    def get_current_player(self) -> Player:
        return self.p1 if self.p1.get_color() == self.turn else self.p2

    def get_turn(self) -> Color:
        return self.turn

    def is_valid_move(self, from_: Cell, to_: Cell) -> bool:
        return to_ in [path[0] for path in self.board.get_valid_moves_from(from_)]

    def move(self, from_: Cell, to_: Cell) -> CellView:
        """Moves pawn from one cell to another.
        Returns:
            CellView: view of cell from which move should be continued or None if it was last move
        """
        beaten_cell, transformed = self.board.move(from_, to_)
        self.board_view.update_view_after_move(from_, to_, beaten_cell)

        if not self.board.has_valid_move(to_) or transformed:
            self.next_round()
            return None

        return self.board_view.get_cell_view(to_)

    def has_valid_move(self, cell_view: CellView) -> bool:
        return self.board.has_valid_move(cell_view.get_cell())
