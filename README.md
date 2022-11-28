# CISC/CMPE 204 Modelling Project - Amy Brons, Alan Teng, Kate Edgar, Dan Munteanu

Manacala Modelling Project

Mancala Description: Mancala is an ancient boardgame where you strategically ‘sow’ and ‘capture’ until you run out of pieces. Played by two people, each player tries to get a higher score by strategically picking and placing game pieces (traditionally stones, but any small object works) around the playing area, which is made up of 12 pits or pockets (six per side) and two stores (larger pockets at the end of each board). To set the game up, four pieces are placed in each of the 12 pits on the board. Once it has been decided who goes first, that player picks up all the pieces from one of the pockets on their side of the board and moving one place to the right, begins depositing a piece in each pocket until they have no more pieces left in their hand. If the player’s last deposit lands in their store, they get another turn. Pieces are not deposited in the opponent’s store. Similarly, if the player’s last deposit lands in an empty pit on their side of the board, they claim all the pieces in pit directly opposite theirs. The game ends when either of the players has six empty pits on their side, winner is determined by who has the most pieces in their respective store.

For our project, we will be modelling the optimal next move for player A, given a randomized board state. 

## Structure

* `documents`: Contains folders for both of your draft and final submissions. README.md files are included in both.
* `run.py`: General wrapper script that you can choose to use or not. Only requirement is that you implement the one function inside of there for the auto-checks.
* `test.py`: Run this file to confirm that your submission has everything required. This essentially just means it will check for the right files and sufficient theory size.
