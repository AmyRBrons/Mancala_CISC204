# Resolver file to play one round, small module functions per step/ action
from board import buildBoard

# Set the board
board = buildboard()


# Set the player to the first player spot
def playerSet(Board):
    playerRow = Board[1]
    return playerRow # returns list of payer pits, ie: [store, 1,2,3,4,5,6]


# Determines the number of gems in a pit
def GemsinPit(board, row, col):
    for row in board:
        for col in row:
            return board[row][col]


# Detects if a pit is empty
def pitIsEmpty(board, n):
    if GemsinPit(board, 1, n) == 0:
        return True
    else:
        return False

def rightMostPit(board, n):
    if board[1][n] == 0:
        return False
    else:
        return True

# Detects if the opposite pit is empty
def oppEmpty(board, n):
    if pitIsEmpty(board, 0, n+1) == True:
        return True
    else:
        return False


# Determines if the player can collect seeds from the opposite pit
def canCollect(board, n):
    # If the pit is empty and the opposite is not, return true
    if (pitIsEmpty(board, n) == True) and (oppEmpty(board, n) == False):
        return True
    else:
        return False


# Determines if the player can collect gems from the opposite pit
def collectOpp(board, n):
    if board[1][n] == 13 and board[0][n+1] != 0:
        return True
    elif board[1][n] == 0 and board[0][n+1] != 0:
        for i in range(6):
            if i == n:
                return False
            if board[1][i] == n-i:
                return True
    else:
        return False


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


# Determines if player A can block player B from depositing their final seed in their store
def blockOpp(board, n):
    for i in range(1, 7):
        if board[0][i] != 0 and board[0][i] == i:  # Testing if player B can deposit a final seed in their store
            if board[1][n] >= (6-n) + (7-i):  # Testing if player A can block
                return True
            else:
                return False


def pitDetermination(board):
    neededValuesFinal = [0, 0, 0, 0, 0, 0]
    neededValuesBlock = [0, 0, 0, 0, 0, 0]
    neededValuesOpp = [0, 0, 0, 0, 0, 0]
    neededValuesRight = [0, 0, 0, 0, 0, 0]

    for i in range(6):
        neededValuesFinal.insert(i, (finalStore(board, i)))  # 1. Putting the final seed in the player store

    finalGemInStore = {
        "pit1A": [1, 0, neededValuesFinal[0]],
        "pit2A": [1, 1, neededValuesFinal[1]],
        "pit3A": [1, 2, neededValuesFinal[2]],
        "pit4A": [1, 3, neededValuesFinal[3]],
        "pit5A": [1, 4, neededValuesFinal[4]],
        "pit6A": [1, 5, neededValuesFinal[5]],
    }

    for j in range(6):
        neededValuesBlock.insert(j, (blockOpp(board, j)))   # 2. Block the opponent from putting a seed in there store

    needBlockOpp = {
        "pit1A": [1, 0, neededValuesBlock[0]],
        "pit2A": [1, 1, neededValuesBlock[1]],
        "pit3A": [1, 2, neededValuesBlock[2]],
        "pit4A": [1, 3, neededValuesBlock[3]],
        "pit5A": [1, 4, neededValuesBlock[4]],
        "pit6A": [1, 5, neededValuesBlock[5]],
    }

    for k in range(6):
        neededValuesOpp.insert(k, collectOpp(board, k))

    needOpp = {
        "pit1A": [1, 0, neededValuesOpp[0]],
        "pit2A": [1, 1, neededValuesOpp[1]],
        "pit3A": [1, 2, neededValuesOpp[2]],
        "pit4A": [1, 3, neededValuesOpp[3]],
        "pit5A": [1, 4, neededValuesOpp[4]],
        "pit6A": [1, 5, neededValuesOpp[5]],
    }

    for m in range(6):
        neededValuesRight.insert(m, rightMostPit(board, m))

    needRight = {
        "pit1A": [1, 0, neededValuesRight[0]],
        "pit2A": [1, 1, neededValuesRight[1]],
        "pit3A": [1, 2, neededValuesRight[2]],
        "pit4A": [1, 3, neededValuesRight[3]],
        "pit5A": [1, 4, neededValuesRight[4]],
        "pit6A": [1, 5, neededValuesRight[5]],
    }

    return needOpp


# Printing the randomized Mancala board
print(' ', *board[0][1:7])
print(board[0][0], '            ', board[1][6])
print(' ', *board[1][0:6])

print(pitDetermination(board))
