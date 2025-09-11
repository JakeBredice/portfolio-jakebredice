class Room:
    def __init__(self, name, description, exits, items=[]):
        self.name = name
        self.description = description
        self.exits = exits
        self.items = items 
    def printexits(self):
        print('Exits:')
        print("\n".join(self.exits))

