"""
Author:         Jake Bredice
Date:           12-4-2024
Assignment:     Project 2: RPG
Course:         CPSC1051
Lab Section:    SECTION 001

CODE DESCRIPTION:
Text-Based Escape Game
"""

from room import Room
from adventure_map import AdventureMap
from inventory import Inventory
from item import Item
from room_not_found_error import RoomNotFoundError

def main():
    print("\nWelcome to the Adkins house! This time you won't be able to leave so easily. Goodluck.")

    # Initialize map w/room storage
    adventure_map = AdventureMap()
    
    # Initialize player inventory 
    inventory = Inventory()
    
    # Initialize Items
    book = Item("Book", "\"A Tale of Two Cities by Charles Dickens\". The greatest novel ever written.", "read", "You skip to the ending to read Sydney Carton's final speech:\n\tIt is a far, far better thing that I do, than I have ever done; it is a far far better rest that I go to than I have ever known.\nWhat a perfect ending...")
    
    
    fork = Item("Fork", "A conveniently pronged eating utensil. Now I just need something to eat.")
    
    pizza_cutter = Item("Pizza Cutter", "This must be left over from the tragedy that occurred at Adkin's Pizzeria")
    
    harmonica = Item("Harmonica", "A mouth organ. This might keep me entertained for a couple of hours.", "play", "You play the sweet sweet melodies of Piano Man on the harmonica. If only someone could hear you...")

    key = Item("Key", "A golden key. This has to unlock something. Right?", "unlock", "You unlock the trapdoor under the bed. You crawl through it and into the real world.\nParadiso awaits.\nCongratulations.")
    
    trophy = Item("Old Trophy", "An old youth bowling league trophy. The words engraved in the plaque are: \"Highest Youth Average: Richard Khouri 186\"")
    
    picture = Item("Picture", "An old picture found on the night stand.", "inspect", "You take a closer look at the picture. It's an old picture of Evan Kessler and Richard Khouri back when they studied at Clemson. Good times.")

    adventure_map.add_room(Room("Guest Room", "A room filled with numerous torture devices. Who said anything about welcome guests?", ['Kitchen'], [harmonica]))
    adventure_map.add_room(Room("Library", "Better version of the study. It has all of the different books that one may want. Make sure that you stay quiet or the mean librarian will slap you!", ["Holodeck", "Trophy Room", "Study"], [book]))
    adventure_map.add_room(Room("Kitchen", "This amazing culinary art studio has it all: cheese cellar, wine racks, and a 16 stove burner. With its pizza oven, it makes for the perfect Italian getaway.", ["Study", "Guest Room"], [fork, pizza_cutter]))
    adventure_map.add_room(Room("Study", "Do you love being disturbed while working? This room has it all. It is the central hub to the whole house. It has a giant wall of computers and amazing lighting, but doors that exit out into numerous different rooms.", ["Kitchen", "Library", "Bedroom"]))
    adventure_map.add_room(Room("Holodeck", "A room that can disguise itself in a variety of ways. Experience a lush, humid rainforest, a speakeasy of the 1920’s, or the dungeons of Cooper Library.", ["Library"], [key]))
    adventure_map.add_room(Room("Trophy Room", "Spacious room with oak wood as far as the eye can see, shelves filled to the brim with trophies and obscure collections, it really makes you wonder who they belong to.", ["Bedroom", "Library"], [trophy]))
    adventure_map.add_room(Room("Bedroom", "A lavished bed adorns the center of this room, with long curtains, beautiful rugs, and gilded furniture acting as little details to truly make this a great bedroom. You see a trapdoor hidden under the bed.", ["Study", "Trophy Room"], [picture]))
   
    # Input variations
    inputs = {"exit": ["exit", "leave"],
              "lookaround": ["look around", "lookaround", "look"],
              "pickup": ["pick up","pickup", "take", "grab"],
              }



    #Setup variables
    current = adventure_map.get_room('Study')  
    actions = 0
    action = ''
    exactions = []
    StillPlaying = True

    print(f"{current.name}: {current.description}")
    current.printexits()
    #Main game loop
    while StillPlaying:
        #Update possible actions
        for item in inventory.items:
            if item.action not in exactions:
                exactions.append(item.action)
        # Update possible extra actions from inventory
        exactions = [item.action for item in inventory.items if item.action != 'unlock']

        # List all valid actions
        valid_actions = ["exit", "look around", "pick up", "inventory"] + exactions
        print('Please choose an action:')
        print('Options:', ', '.join(valid_actions))

        action = input().strip().lower()
        actions += 1
        #Exit handler
        if action in ["exit", "leave"]:
            print('Where would you like to go?')
            troom = input()
            try:
                troom = troom.title()
                if troom not in current.exits:
                    raise RoomNotFoundError(troom)
                current = adventure_map.get_room(troom)
                print(f"{current.name}: {current.description}")
                current.printexits()
            except RoomNotFoundError:
                print(f'Invalid Room: {troom} -> Room not found')    
        #Look handler        
        elif action in ["look around", "lookaround", "look"]:
            print(f'{current.description}')
            if len(current.items) < 1:
                print('You find some items around you: There are no items around here.')
            else:
                print(f'You find some items around you: {", ".join([item.name for item in current.items])}.')
        # Pickup handler
        elif action in ["pick up","pickup", "take", "grab"]:
            try:
                item = current.items[0]
                print(f'Picked up {item.name}.')
                inventory.add_item(current.items.pop(0))
            except IndexError:
                print('No more items here')
        #Inventory handler
        elif action == 'inventory':
            print(inventory.view())
        #Extra actions handler
        elif action in exactions and action !='unlock':
            for item in inventory.items:
                if item.action == action:
                    print(item.content)
        #Winning handler
        elif (action.lower() == 'unlock') and current.name == 'Bedroom':
            for item in inventory.items:
                if item.action == action:
                    print(item.content)
            StillPlaying = False
        #Extra actions not possible handler
        elif action.lower() in ['read', 'inspect', 'play', 'unlock']:
            print(f'I don\'t have anything to {action.lower().strip()}.')
        #Invalid input handler
        else:
            print(f'I don\'t know the word \"{action}\".')
    #Write gamelog file
    f = open('gamelog.txt', 'w')
    f.write(f'Congratulations! You finished the game in {actions} steps.')
    f.write('\n')
    f.close()


        




if __name__ == "__main__":
    main()
