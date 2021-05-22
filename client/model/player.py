from utils.color import Color


class Player:
    def __init__(self, email: str, color: Color = None):
        self.email = email
        self.in_game = False
        self.color = color

    def join_game(self, as_who: Color) -> None:
        self.in_game = True
        self.color = as_who

    def get_color(self) -> Color:
        return self.color

    def get_email(self) -> str:
        return self.email

    def leave_game(self) -> None:
        self.in_game = False
