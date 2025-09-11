class RoomNotFoundError(Exception):
    def __init__(self, room):
        self.room = room
        