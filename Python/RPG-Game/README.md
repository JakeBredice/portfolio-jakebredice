# RPG Escape Game

**Description:**  
Text-based RPG escape game where the player navigates the Adkins house, collects items, and completes extra actions to escape. Rooms are interconnected and some actions/items are required to unlock the final exit.

**Skills Demonstrated:**  
Object-oriented programming, input validation, game logic, Python classes, loops, conditionals, user input handling.

**Features:**  
- Multiple rooms with descriptions and exits  
- Item collection and inventory management  
- Extra actions based on items (e.g., read, inspect, play, unlock)  
- Winning condition using a key item  

## How to Run
1. Make sure you have Python 3 installed.  
2. Navigate to this folder in a terminal.  
3. Run the main script:
```bash
python main.py
```

## Example Gameplay
```

Welcome to the Adkins house! This time you won't be able to leave so easily. Goodluck.
Study: Do you love being disturbed while working? Exits: Kitchen, Library, Bedroom
Please choose an action:
Options: exit, look around, pick up, inventory
look around
You find some items around you: There are no items around here.
exit
Where would you like to go?
bedroom
Bedroom: A lavished bed with a hidden trapdoor. Exits: Study, Trophy Room
pickup
Picked up Picture.
inspect
You take a closer look at the picture. Good times.
inventory
INVENTORY: Picture
exit
Where would you like to go?
kitchen
Kitchen: Amazing culinary art studio. Exits: Study, Guest Room
pickup
Picked up Fork.
Picked up Pizza Cutter.
inventory
INVENTORY: Picture, Fork, Pizza Cutter
exit
Where would you like to go?
guest room
Guest Room: Room filled with numerous torture devices. Exits: Kitchen
pickup
Picked up Harmonica.
play
You play the sweet sweet melodies of Piano Man on the harmonica.
exit
Where would you like to go?
library
Library: Better version of the study. Exits: Holodeck, Trophy Room, Study
pickup
Picked up Book.
read
You skip to the ending to read Sydney Carton's final speech. What a perfect ending...
exit
Where would you like to go?
holodeck
Holodeck: Room that can disguise itself. Exits: Library
pickup
Picked up Key.
inventory
INVENTORY: Picture, Fork, Pizza Cutter, Harmonica, Book, Key
exit
Where would you like to go?
trophy room
Trophy Room: Spacious room with shelves of trophies. Exits: Bedroom, Library
exit
Where would you like to go?
bedroom
Bedroom: Lavished bed with a hidden trapdoor. Exits: Study, Trophy Room
unlock
You unlock the trapdoor under the bed. You crawl through it and into the real world.
Paradiso awaits. Congratulations.
```