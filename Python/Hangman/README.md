# Hangman

**Description:**  
Text-based Hangman game where one player guesses letters to uncover a hidden word. Tracks incorrect guesses and ends when the word is guessed or the maximum number of incorrect attempts is reached.

**Skills Demonstrated:**  
Loops, conditionals, string manipulation, input validation, lists.

**Features:**  
- Tracks correct and incorrect guesses  
- Displays current word state after each guess  
- Limits number of incorrect guesses  
- Simple text-based interface  

## How to Run
1. Make sure you have Python 3 installed.  
2. Navigate to this folder in a terminal.  
3. Run the main script:
python main.py

## Example Gameplay
Please enter a seed:
67
Let's play Hangman!
You are going to be given some empty dashes and you will guess the word in question by typing one letter at a time.
Well... that is before you are hanged!

The category is: places

        +---+
        |   |
            |
            |
            |
            |
        =========

_______
Guess a letter:
p
There are no p's

        +---+
        |   |
        O   |
            |
            |
            |
        =========

_______
Guess a letter:
a
Correct!

        +---+
        |   |
        O   |
            |
            |
            |
        =========

____a__
Guess a letter:
u
There are no u's

        +---+
        |   |
        O   |
        |   |
            |
            |
        =========

____a__
Guess a letter:
h
Correct!

        +---+
        |   |
        O   |
        |   |
            |
            |
        =========

_h__a__
Guess a letter:
c
Correct!

        +---+
        |   |
        O   |
        |   |
            |
            |
        =========

ch_ca__
Guess a letter:
i
Correct!

        +---+
        |   |
        O   |
        |   |
            |
            |
        =========

chica__
Guess a letter:
g
Correct!

        +---+
        |   |
        O   |
        |   |
            |
            |
        =========

chicag_
Guess a letter:
o
Correct!

        +---+
        |   |
        O   |
        |   |
            |
            |
        =========

chicago
You have won!

        +---+
        |   |
        O   |
        |   |
            |
            |
        =========

chicago
You have won!