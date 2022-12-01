# File to create randomized board
import random


# Builds randomized board
def buildBoard():
    player = 0
    playerAstore = 0  # Zero gems in the stores to start
    playerBstore = 0
    board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]

    # Randomly fills in player A's gems
    playerA1 = random.randint(0, 24)
    playerA2range = 24 - playerA1
    playerA2 = random.randint(0, playerA2range)
    playerA3range = playerA2range-playerA2
    playerA3 = random.randint(0, playerA3range)
    playerA4range = playerA3range - playerA3
    playerA4 = random.randint(0, playerA4range)
    playerA5range = playerA4range - playerA4
    playerA5 = random.randint(0, playerA5range)
    playerA6 = playerA5range - playerA5

    # Randomly fills player B's gems
    playerB1 = random.randint(0, 24)
    playerB2range = 24 - playerB1
    playerB2 = random.randint(0, playerB2range)
    playerB3range = playerB2range-playerB2
    playerB3 = random.randint(0, playerB3range)
    playerB4range = playerB3range - playerB3
    playerB4 = random.randint(0, playerB4range)
    playerB5range = playerB4range - playerB4
    playerB5 = random.randint(0, playerB5range)
    playerB6 = playerB5range - playerB5

    # Set board
    board = [[playerBstore, playerB1, playerB2, playerB3, playerB4, playerB5range, playerB6],
             [playerA1, playerA2, playerA3, playerA4, playerA5, playerA6, playerAstore]]
    return board


# Using fully randomized board for testing purposes
# Give the user allowance to fill pits with stones
#pit1 = int(input('Please enter the number of gems in pit 1 (please note you only have 24 gems to split between these 6 pits.)'))
#Board[player][1] = pit1
#pit2 = int(input('Please enter the number of gems in pit 2 (please note you only have', 24-pit1,'gems left)'))
#Board[player][2] = pit2
#pit3 = int(input('Please enter the number of gems in pit 3 (please note you only have', 24-pit1-pit2, 'gems left)'))
#Board[player][1] = pit3
#pit4 = int(input('Please enter the number of gems in pit 4 (please note you only have', 24-pit1-pit2-pit3,'gems left)'))
#Board[player][2] = pit4
#pit5 = int(input('Please enter the number of gems in pit 5 (please note you only have', 24-pit1-pit2-pit3-pit4, 'gems left)'))
#Board[player][2] = pit5
#pit6 = int(input('Please enter the number of gems in pit 6 (please note you only have', 24-pit1-pit2-pit3-pit4, 'gems left)'))
#Board[player][1] = pit6

