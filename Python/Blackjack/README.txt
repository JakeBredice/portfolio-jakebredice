# Blackjack

**Description:**  
Text-based Blackjack game supporting 1+ players, with seed-based reproducibility for deterministic card draws. Players can hit or stick, bust detection is implemented, and the winner is automatically calculated.

**Skills Demonstrated:**  
Object-oriented programming, input validation, game logic, Python classes, loops, conditionals, user input handling.

**Features:**  
- Seed-based reproducibility  
- Multiplayer support (1+ players)  
- Hit or stick decisions  
- Bust detection  
- Automatic winner calculation

## How to Run
1. Make sure you have Python 3 installed.  
2. Navigate to this folder in a terminal.  
3. Run the main script:
python main.py

## Example Gameplay
Give me a seed:
67
How many players would you like to play with?
3
Player 1's cards:
['5H', '9H']
Acknowledge that you have seen your cards player 1 by entering any key.
q
Player 2's cards:
['KS', '3C']
Acknowledge that you have seen your cards player 2 by entering any key.
q
Player 3's cards:
['7C', '4C']
Acknowledge that you have seen your cards player 3 by entering any key.
q
Now that everyone knows their cards, let's play!
Player 1's cards:
['5H', '9H']
Player 1 would you like to hit or stick?
hit
Player 1's cards:
['5H', '9H', '7D']
Player 1 would you like to hit or stick?
stick
Player 2's cards:
['KS', '3C']
Player 2 would you like to hit or stick?
hit
Player 2's cards:
['KS', '3C', '6S']
Player 2 would you like to hit or stick?
stick
Player 3's cards:
['7C', '4C']
Player 3 would you like to hit or stick?
hit
Player 3's cards:
['7C', '4C', '8C']
Player 3 would you like to hit or stick?
hit
Player 3's cards:
['7C', '4C', '8C', 'KC']
Player 3 you have busted. Enter any key to acknowledge this.
d
Player 3 has busted.
Player 1 got the highest score of 21.