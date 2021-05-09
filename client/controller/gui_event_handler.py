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

        self.hovered_cell = None

    def on_mouse_enter(self, event: Event, emitter: CellView) -> None:
        player = self.game_engine.get_current_player()

        if not emitter.has_pawn() or emitter.get_pawn_color() != player.get_color():
            return

        self.hovered_cell = emitter
        self.board_view.highlight_valid_cells(emitter)

    def on_mouse_out(self, event: Event, emitter: EventEmitter) -> None:
        self.board_view.clear_highlight()
