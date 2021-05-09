from model.board import Board
from view.board_view import BoardView
from view.game_view import GameView
from utils.color import Color
from model.player import Player


class GameEngine:
    def __init__(self):
        self.p1 = Player('kntp1')
        self.p2 = Player('kntp2')

        self.p1.join_game(Color.WHITE)
        self.p2.join_game(Color.BLACK)

        self.board = Board()
        self.board_view = BoardView(self.board, 640, 640, True)
        self.board_view.draw()

        self.game_view = GameView(self.board_view, 400, 400, 800, 800)
        self.turn = Color.WHITE

        self.board.update_valid_moves(self.turn)
        for move_list in self.board.get_valid_moves().values():
            print(move_list)

    def next_round(self):
        self.turn = Color.reverse(self.turn)

    def get_board_view(self) -> BoardView:
        return self.board_view

    def get_current_player(self) -> Player:
        return self.p1 if self.p1.get_color() == self.turn else self.p2
