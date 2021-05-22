from PyQt5.QtWidgets import QDialog, QFrame, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QCursor
from model.board import Board
from view.board_view import BoardView
from utils.event_emitter import EventEmitter, Event


class GameWindow(QDialog, EventEmitter):
    def __init__(self, x: int, y: int, width: int, height: int,
                 board_width: int, board_height: int, title: str = 'Checkers'):
        super().__init__()

        self.board_width = board_width
        self.board_height = board_height
        self.title = title

        self.your_move_msg = 'Your Move!'
        self.enemy_move_msg = 'Enemy Move...'
        self.secs = 0

        self.board_view = None

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setGeometry(x, y, width, height)
        self.setWindowTitle(title)

    def restart(self) -> "GameWindow":
        rect = self.geometry()
        res = GameWindow(rect.x(), rect.y(), rect.width(), rect.height(),
                         self.board_width, self.board_height, self.title)

        for event, listeners in self.listeners.items():
            for listener in listeners:
                res.add_event_listener(event, listener)

        return res

    def draw_board(self, board: Board, white_bottom: bool) -> BoardView:
        self.board_view = BoardView(
            board, self.board_width, self.board_height, white_bottom)
        self.board_view.draw()
        self.layout.addWidget(self.board_view)
        self._draw_info_widget()
        return self.board_view

    def _draw_info_widget(self) -> None:
        self.info = QFrame()
        self.info.setObjectName('game-info')
        layout = QVBoxLayout(self.info)
        self.layout.setAlignment(layout, Qt.AlignTop)

        title = QFrame()
        t_layout = QVBoxLayout(title)
        for c in ('Checkers', 'Online'):
            l = QLabel(c)
            t_layout.addWidget(l, alignment=Qt.AlignCenter)

        title.setObjectName('gtitle')
        layout.addWidget(title, alignment=Qt.AlignCenter)

        self.status_label = QLabel('Waiting For Enemy...')
        self.status_label.setObjectName('status')
        layout.addWidget(self.status_label, alignment=Qt.AlignCenter)
        self.status_label.setGraphicsEffect(self._get_shadow())

        stats = self._build_stats_grid()
        layout.addWidget(stats, alignment=Qt.AlignCenter)

        self.dc_btn = QPushButton('Disconnect')
        self.dc_btn.setGraphicsEffect(self._get_shadow())
        self.dc_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.dc_btn.setObjectName('dc-btn')
        self.dc_btn.clicked.connect(
            lambda: self.call_listeners(Event.LEAVE_ROOM))
        layout.addWidget(self.dc_btn, alignment=Qt.AlignCenter)

        self.layout.addWidget(self.info)

    def _build_stats_grid(self) -> QFrame:
        keys = ['enemy', 'time', 'round', 'y_score', 'e_score', 'last_move']
        text_contents = ['Enemy', 'Time', 'Round', 'Your Score',
                         'Enemy Score',  'Last Move']
        defaults = ['waiting...', '0', '0', '0', '0', 'None']

        self.stats = {k: QLabel(v) for k, v in zip(keys, defaults)}

        comp = QFrame()
        comp.setGraphicsEffect(self._get_shadow())
        comp.setObjectName('stats')
        layout = QVBoxLayout(comp)

        for i, (key, text) in enumerate(zip(keys, text_contents)):
            sub_comp = QFrame()
            sub_layout = QHBoxLayout(sub_comp)
            label = QLabel(text)
            sub_layout.addWidget(label, alignment=Qt.AlignLeft)
            sub_layout.addWidget(self.stats[key], alignment=Qt.AlignCenter)
            layout.addWidget(sub_comp)

        return comp

    def _get_shadow(self) -> QGraphicsDropShadowEffect:
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(6)
        shadow.setOffset(5)
        shadow.setColor(QColor(0, 0, 0, 100))
        return shadow

    def update_score(self, owner_score: int, enemy_score: int) -> None:
        self.stats['y_score'].setText(str(owner_score))
        self.stats['e_score'].setText(str(enemy_score))

    def set_last_move(self, move: str) -> None:
        self.stats['last_move'].setText(move)

    def enemy_joined(self, email: str) -> None:
        self.stats['enemy'].setText(email)
        self.status_label.setText(self.your_move_msg)

    def set_enemy(self, email: str) -> None:
        self.stats['enemy'].setText(email)
        self.status_label.setText(self.enemy_move_msg)

    def next_round(self) -> None:
        if self.status_label.text() == self.enemy_move_msg:
            self.status_label.setText(self.your_move_msg)
        else:
            self.status_label.setText(self.enemy_move_msg)

        self.stats['round'].setText(str(int(self.stats['round'].text()) + 1))

    def update_time(self) -> None:
        self.secs += 1
        secs = self.secs % 60
        mins = self.secs // 60
        self.stats['time'].setText(
            f'{mins if mins > 9 else f"0{mins}"}:{secs if secs > 9 else f"0{secs}"}')
