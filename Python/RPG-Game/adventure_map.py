from room import Room
from room_not_found_error import RoomNotFoundError

class AdventureMap:
    def __init__(self):
        self.rooms = {}

    def add_room(self, room):
        self.rooms[room.name] = room

    def get_room(self, room_name):
        if room_name not in self.rooms:
            raise RoomNotFoundError(room_name)
        return self.rooms[room_name]
