"""
Author:         Jake Bredice
Date:           10-27-2024
Assignment:     Lab 07
Course:         CPSC1051
Lab Section:    SECTION 101

CODE DESCRIPTION:

"""

import random

def printupdatedman(wrong):
    """
    Print current hangman
    Args:
        wrong: int of how many incorrect guesses
    Returns:
        nothing
    """
    stages = [
        """
        +---+
        |   |
            |
            |
            |
            |
        =========
        """,
        """
        +---+
        |   |
        O   |
            |
            |
            |
        =========
        """,
        """
        +---+
        |   |
        O   |
        |   |
            |
            |
        =========
        """,
        """
        +---+
        |   |
        O   |
       /|   |
            |
            |
        =========
        """,
        """
        +---+
        |   |
        O   |
       /|\\ |
            |
            |
        =========
        """,
        """
        +---+
        |   |
        O   |
       /|\\ |
       /    |
            |
        =========
        """,
        """
        +---+
        |   |
        O   |
       /|\\ |
       / \\ |
            |
        =========
        """,
    ]
    print(stages[wrong])

def playerguess(guesses, ritem, blanks, wrong):
    """
    Asks for player guess, handles errors, and evaluates correctness
    Args:
        guesses: list of letters already guessed
        ritem: random string selected at beginning of game
        blanks: Current blank message with correctly guessed characters filled in
        wrong: int of how many incorrect guesses
    Returns:
        wrong
    """
    print("Guess a letter: ")
    guess = input().lower().strip()
    bindexs = []
    while len(guess) > 1:
        print("Please enter in just a singular letter")
        guess = input().lower().strip()
    while guess in guesses:
        print("You have already guessed that letter!")
        guess = input().lower().strip()
    while len(guess) > 1:
        print("Please enter in just a singular letter")
        guess = input().lower().strip()
    while guess in guesses:
        print("You have already guessed that letter!")
        guess = input().lower().strip()
    while len(guess) > 1:
        print("Please enter in just a singular letter")
        guess = input().lower().strip()
    guesses.append(guess)
    if guess in ritem:
        print('Correct!')
        for i in range(len(ritem)):
            if ritem[i] == guess:
                bindexs.append(i)
        for i in bindexs:
            blanks[i] = guess
        checkdone(blanks, wrong, ritem)
    else:
        print(f"There are no {guess}'s")
        wrong += 1
    return wrong
def checkdone(blanks, wrong, ritem):
    """
    Checks if game is finished due to wnning or losing
    Args:
        ritem: random string selected at beginning of game
        blanks: Current blank message with correctly guessed characters filled in
        wrong: int of how many incorrect guesses
    Returns:
        False unless game is over
    """
    if '_' not in blanks:
        printupdatedman(wrong)
        print(ritem)
        print("You have won!")
        return True
    elif wrong >= 6:
        print("Gave Over, you are HANGED!")
        print(f"The word was: {ritem}")
        print("Better luck next time.")
        return True
    return False

categories = {
    'places': ['New York', 'Los Angeles', 'California', 'Chicago', 'Illinois',  
        'Houston', 'Texas', 'Philadelphia', 'Pennsylvania', 'Phoenix', 'Arizona', 'San Antonio', 
        'San Diego', 'Dallas', 'San Jose', 'Austin', 'Texas', 'Jacksonville', 'Florida', 
        'San Francisco', 'Indianapolis', 'Indiana', 'Massachusetts', 'Mississippi'],
    'movies': ["The Godfather", "The Shawshank Redemption", "Schindler's List",
        "Raging Bull", "Casablanca", "Citizen Kane", "Gone With The Wind", "The Wizard Of Oz",
        "Inception"],
    "ta": ["Richard", "John", "Mars", "Aaron", "Brendan", "Jada", "Braylon"]
}
def main():

    print("Please enter a seed: ")
    seed = int(input())
    random.seed(seed)
    wrong = 0
    guesses = []

    print("Let's play Hangman!")
    print("You are going to be given some empty dashes and you will guess the word in question by typing one letter at a time.")
    print("Well... that is before you are hanged!\n")

    ckeys = list(categories.keys())
    rckey = ckeys[random.randint(0, len(ckeys) - 1)]
    rcitems = categories[rckey]
    ritem = rcitems[random.randint(0, len(rcitems) - 1)].lower()

    blanks = ['_' if char != ' ' else ' ' for char in ritem]
    print(f"The category is: {rckey}\n")
    while wrong <= 6:
        printupdatedman(wrong)
        print(''.join(blanks))
        wrong = playerguess(guesses, ritem, blanks, wrong)
        if checkdone(blanks, wrong, ritem):
            break


# Runs main.
if __name__ == "__main__":
    main()
