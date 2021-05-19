from model.board import Board
from model.cell import Cell
from view.board_view import BoardView
from view.cell_view import CellView
from view.game_window import GameWindow
from utils.color import Color
from model.player import Player
from utils.event_emitter import EventEmitter
from utils.events import Event
from typing import Tuple


class GameEngine(EventEmitter):
    def __init__(self, game_window: GameWindow, owner: Player, guest: Player = None):
        super().__init__()
        self.owner = owner
        self.guest = guest
        self.owner.join_game(Color.WHITE)
        if guest is not None:
            self.guest.join_game(Color.BLACK)

        self.board = Board()
        self.game_window = game_window
        self.board_view = self.game_window.draw_board(self.board)

        self.turn = Color.WHITE

        self.board.update_valid_moves(self.turn)

    def next_round(self):
        self.turn = Color.reverse(self.turn)
        self.board.update_valid_moves(self.turn)

    def set_guest(self, guest: Player) -> None:
        self.guest = guest
        self.guest.join_game(Color.BLACK)

    def get_board_view(self) -> BoardView:
        return self.board_view

    def get_current_player(self) -> Player:
        return self.owner if self.owner.get_color() == self.turn else self.guest

    def get_turn(self) -> Color:
        return self.turn

    def is_valid_move(self, from_: Cell, to_: Cell) -> bool:
        return to_ in [path[0] for path in self.board.get_valid_moves_from(from_)]

    def move(self, from_: Cell, to_: Cell, enemy_move: bool = False) -> CellView:
        """Moves pawn from one cell to another.
        Returns:
            CellView: view of cell from which move should be continued or None if it was last move
        """
        beaten_cell, transformed = self.board.move(from_, to_)
        self.board_view.update_view_after_move(from_, to_, beaten_cell)
        move_data = {
            'from': from_.get_position(),
            'to': to_.get_position(),
            'beaten': beaten_cell.get_position() if beaten_cell is not None else (-1, -1)
        }

        if not self.board.has_valid_move(to_) or transformed:
            move_data['last_move'] = True
            if not enemy_move:
                self.call_listeners(Event.PLAYER_MOVED, move_data)
            self.next_round()
            return None

        move_data['last_move'] = False
        if not enemy_move:
            self.call_listeners(Event.PLAYER_MOVED, move_data)

        return self.board_view.get_cell_view(to_)

    def update_enemy_move(self, from_: Tuple[int, int], to_: Tuple[int, int]):
        from_ = self.board.get_cell(*from_)
        to_ = self.board.get_cell(*to_)
        self.move(from_, to_, enemy_move=True)

    def has_valid_move(self, cell_view: CellView) -> bool:
        return self.board.has_valid_move(cell_view.get_cell())

    def is_running(self) -> bool:
        """returns true if 2 players have joined"""
        return self.guest is not None
