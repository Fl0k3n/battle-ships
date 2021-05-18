from typing import Dict


class Room:
    def __init__(self, idx: int, owner_email: str, guest_email: str = None):
        self.idx = idx
        self.owner_email = owner_email
        self.guest_email = guest_email

    def is_joinable(self) -> bool:
        return self.guest_email is None

    @staticmethod
    def from_json(json_data: Dict[str, str]) -> "Room":
        idx = json_data['id']
        owner = json_data['owner']
        guest = json_data.get('guest')
        return Room(idx, owner, guest)
