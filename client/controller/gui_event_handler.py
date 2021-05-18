from controller.game_engine import GameEngine
from typing import Iterable
from utils.events import Event
from utils.event_emitter import EventEmitter
from view.board_view import BoardView
from view.cell_view import CellView


class GuiEventHandler:
    def __init__(self, game_engine: GameEngine):
        self.game_engine = game_engine
        self.board_view = game_engine.get_board_view()

        for cell_view in self.board_view.get_cell_views():
            cell_view.add_event_listener(
                Event.MOUSE_ENTERED, self.on_mouse_enter)

            cell_view.add_event_listener(Event.MOUSE_LEFT, self.on_mouse_out)

            cell_view.add_event_listener(
                Event.CELL_CLICKED, self.on_cell_clicked)

        self.hovered_cell = None
        self.clicked_cell = None
        self.move_initiated = False  # if player has already choosen path

    # GAME GUI EVENTS
    def on_mouse_enter(self, event: Event, emitter: CellView) -> None:
        turn = self.game_engine.get_turn()

        if self.move_initiated or not emitter.has_pawn() or\
                emitter.get_pawn_color() != turn or self.clicked_cell is not None:
            return

        self.hovered_cell = emitter
        self.board_view.highlight_valid_cells(emitter)

    def on_mouse_out(self, event: Event, emitter: CellView) -> None:
        if not self.move_initiated and self.clicked_cell is None:
            self.board_view.clear_highlight()

    def on_cell_clicked(self, event: Event, emitter: CellView) -> None:
        turn = self.game_engine.get_turn()

        if emitter.has_pawn() and emitter.get_pawn_color() == turn:
            if self.clicked_cell == emitter:
                self.clicked_cell = None
            elif self.game_engine.has_valid_move(emitter):
                self.board_view.clear_highlight()
                self.board_view.highlight_valid_cells(emitter)
                self.clicked_cell = self.hovered_cell = emitter

        elif self.clicked_cell is not None and \
                self.game_engine.is_valid_move(self.clicked_cell.get_cell(), emitter.get_cell()):
            self.move_initiated = True
            self.board_view.clear_highlight()

            next_cell = self.game_engine.move(
                self.clicked_cell.get_cell(), emitter.get_cell())

            if next_cell is not None:
                self.hovered_cell = self.clicked_cell = next_cell
                self.board_view.highlight_valid_cells(next_cell)
            else:
                self.move_initiated = False
                self.hovered_cell = self.clicked_cell = None
        else:
            print('invalid')

    # AUTH GUI EVENTS
