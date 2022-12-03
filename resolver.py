# Resolver file to play one round, small module functions per step/ action
from board import buildBoard

# Set the board
board = buildBoard()


# Determines if the final gem of a given pit will land in player A's store
def finalStore(board, n):
    if board[1][n] == 0:  # Pit cannot be empty
        return False
    else:
        maxGemsToStore = 19-n  # Need 19 gems to get from furthest pit to store
        if board[1][n] == 6-n:
            return True
        elif maxGemsToStore == board[1][n]:  # Maximum number of gems needed to iterate around the board once
            return True
        else:
            return False


# Determines if player A can block player B from depositing their final gem in their store
def blockOpp(board, n):
    for i in range(1, 7):
        if board[0][i] != 0 and board[0][i] == i:  # Testing if player B can deposit a final gem in their store
            if board[1][n] >= (6-n) + (7-i):  # Testing if player A can block
                return True
            else:
                return False


# Determines if the player can collect gems from the opposite pit
def collectOpp(board, n):
    if board[1][n] == 13 and board[0][n+1] != 0:  # Player needs 13 gems for the final gem to land in the original store. Opposite pit cannot be empty
        return True
    elif board[1][n] == 0 and board[0][n+1] != 0:  # Pit on player's side needs to be empty, opposite pit cannot be empty
        for i in range(6):  # Testing if there are gems in a pit on the player's side which can be moved so that the final gem will land in the empty pit
            if i == n: 
                return False
            if board[1][i] == n-i:
                return True
    else:
        return False


# Move the gems in the right most non zero pit
def rightMostPit(board, n):
    if board[1][n] == 0:  # Pit cannot be empty
        return False
    else:
        return True


# Tests strategies on all the pits on player A's side. Returns dictionary of boolean mappings for each strategy
def pitDetermination(board):
    neededValuesFinal = [None, None, None, None, None, None]
    neededValuesBlock = [None, None, None, None, None, None]
    neededValuesOpp = [None, None, None, None, None, None]
    neededValuesRight = [None, None, None, None, None, None]

    for i in range(6):  # Testing strategies on every pit on player A's side
        neededValuesFinal.insert(i, (finalStore(board, i)))  # 1. Putting the final gem in player A's store
        neededValuesBlock.insert(i, (blockOpp(board, i)))   # 2. Block player B from putting their final gem in their store
        neededValuesOpp.insert(i, collectOpp(board, i))  # 3. Collect gems from the opposite pit
        neededValuesRight.insert(i, rightMostPit(board, i))  # 4. Moves right most non-zero gems

    # Truth values for dropping the final gem in player A's store
    finalGemInStore = {
        "pit1A": [1, 0, neededValuesFinal[0]],
        "pit2A": [1, 1, neededValuesFinal[1]],
        "pit3A": [1, 2, neededValuesFinal[2]],
        "pit4A": [1, 3, neededValuesFinal[3]],
        "pit5A": [1, 4, neededValuesFinal[4]],
        "pit6A": [1, 5, neededValuesFinal[5]],
    }

    # Truth values for blocking player B from dropping their final gem in their store
    blockOpponent = {
        "pit1A": [1, 0, neededValuesBlock[0]],
        "pit2A": [1, 1, neededValuesBlock[1]],
        "pit3A": [1, 2, neededValuesBlock[2]],
        "pit4A": [1, 3, neededValuesBlock[3]],
        "pit5A": [1, 4, neededValuesBlock[4]],
        "pit6A": [1, 5, neededValuesBlock[5]],
    }

    # Truth values for collecting gems from the opposite pit
    collectFromOpp = {
        "pit1A": [1, 0, neededValuesOpp[0]],
        "pit2A": [1, 1, neededValuesOpp[1]],
        "pit3A": [1, 2, neededValuesOpp[2]],
        "pit4A": [1, 3, neededValuesOpp[3]],
        "pit5A": [1, 4, neededValuesOpp[4]],
        "pit6A": [1, 5, neededValuesOpp[5]],
    }

    # Truth values for if a pit is not empty
    moveRightGems = {
        "pit1A": [1, 0, neededValuesRight[0]],
        "pit2A": [1, 1, neededValuesRight[1]],
        "pit3A": [1, 2, neededValuesRight[2]],
        "pit4A": [1, 3, neededValuesRight[3]],
        "pit5A": [1, 4, neededValuesRight[4]],
        "pit6A": [1, 5, neededValuesRight[5]],
    }


# Printing the randomized Mancala board
print(' ', *board[0][1:7])
print(board[0][0], '            ', board[1][6])
print(' ', *board[1][0:6])
