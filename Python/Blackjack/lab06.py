"""
Author:         Jake Bredice
Date:           10-21-2024
Assignment:     Lab 06
Course:         CPSC1051
Lab Section:    SECTION

CODE DESCRIPTION:

"""
import random

def get_sum(hand: list) -> int:
    """ Gets the sum of the cards in the players hand.

    Args:
        hand: A list containing the cards in the player's hand.

    Return:
        The sum of the cards in the player's hand.
    """
    total = 0
    aces = 0
    for card in hand:
        total += get_card_value(card, total)
        if card[0] == 'A':
            aces +=1
    while (total > 21) and (aces > 0):
        total -= 10
        aces -= 1
    return total

def get_card_value(card: str, current_total: int) -> int:
    """ Gets the value of the card given the player's hand.

    Args:
        card: The string containing what the card is.
        hand: A list containing the cards in the player's hand.

    Return:
        The value of the card.
    """
    if card[0] in "JQK":
        return 10
    elif card[0] == "A":
        return 11
    else:
        return int(card[:-1])
    
def deal(deck: list) -> list:
    """ Deals 2 cards to each player

    Args:
        deck: A list containing the entire deck of cards.
    
    Return:
        A list containing a hand of two cards.
    """
    hand=[]
    for i in range(2):
        index = random.randint(0, len(deck)-1)
        hand.append(deck[index])
        del deck[index]

    return hand


def hit(deck: list, hand: list) -> None:
    """ Adds one card to the players hand when they hit and removes it from the deck.

    Args:
        deck: A list containing the entire deck of cards.
        hand: A list containing the player's hand.
    
    Return:
        None
    """
    index = random.randint(0, len(deck)-1)
    hand.append(deck[index])
    del deck[index]

    

# Where your main program logic goes.
def main() -> None:
    # List of the deck of cards.
    deck = [
        "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH",
        "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD",
        "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC",
        "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS"
    ]

    print("Give me a seed:")
    s = int(input())
    random.seed(s)
    print("How many players would you like to play with?")
    players = int(input())
    while players <= 0:
        print("Please enter a value greater than 0: ")
        players = int(input())

    hands = []
# Deal to all players hands is a list of lists because deal returns a list also
    for i in range(players):
        hands.append(deal(deck))
        print(f'Player {i + 1}\'s cards:')
        print(hands[i])
        print(f"Acknowledge that you have seen your cards player {i + 1} by entering any key.")
        input()

    print("Now that everyone knows their cards, let's play!")
    scores = [0] * players
#iterate between every players turn
    for i in range(players):
        b = 0
        c = ''
#iterate until player busts or sticks
        while b < 1:
            print(f"Player {i + 1}'s cards:")
            print(hands[i])
            print(f"Player {i + 1} would you like to hit or stick?")
            e = input().lower()
#check validity of input
            while e.lower() not in ['hit', 'stick']:
                print("Invalid input. Please enter either hit or stick: ")
                e = input()
            if e.lower() == "hit":
                hit(deck, hands[i])
                if get_sum(hands[i]) > 21:
                    print(f"Player {i + 1}'s cards:")
                    print(hands[i])
                    print(f"Player {i + 1} you have busted. Enter any key to acknowledge this.")
                    input()
                    scores[i] = 0 
                    b += 1
            elif e.lower() == "stick":
                scores[i] = get_sum(hands[i]) 
                b += 1
#say who busted
    for i in range(len(scores)):
        if scores[i] == 0:
            print(f'Player {i+1} has busted.')
#find indices of winners
    max_indices = []
    max_score = max(scores)
    for i in range(len(scores)):
        if scores[i] == max_score:
            max_indices.append(i)
#final message
    if max_score == 0: 
        print("Nobody won.")
    elif len(max_indices) == 1:
        print(f'Player {max_indices[0] + 1} got the highest score of {max_score}.')  # Use +1 for player number
    else:
        print(f"Players {max_indices[0]+1} and {max_indices[1]+1} tied for the highest score of {max_score}.")
# Runs main.
if __name__ == "__main__":
    main()