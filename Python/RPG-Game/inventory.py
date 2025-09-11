class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def view(self):
        if not self.items:
            return "INVENTORY:"
        return "INVENTORY:\n\t  " + "\n\t  ".join([f"{item.name}- {item.description}" for item in self.items])
            

