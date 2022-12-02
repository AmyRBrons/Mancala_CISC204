# Resolver file to play one round, small module functions per step/ action
from board import buildBoard

# Set the board
board = buildBoard()


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


# Determines if the player can collect seeds from the opposite pit
def collectOpp(board, n):
    if board[1][n] == 0 and board[0][n+1] != 0:
        for i in range(6):
            if i == n:
                continue
            if board[1][i] == n-i:
                return True
            # Needs >6 gem implementation


# Determines if the final gem of a given pit will land in player A's store
def finalStore(board, n):
    if board[1][n] != 0:  # Pit cannot be empty
        maxGemsToStore = 19-n  # Need 19 gems to get from furthest pit to store
        if board[1][n] == 6-n:
            return True
        elif maxGemsToStore == board[1][n]:  # Maximum number of gems needed to iterate around the board once
            return True
        else:
            return False


# Determines if player A can block player B from depositing their final seed in their store
def blockOpp(board, n):
    # Greater than value
    for i in range(1, 7):
        if board[0][i] != 0 and board[0][i] == i:  # Testing if player B can deposit a final seed in their store
            if board[1][n] >= (6-n) + (7-i): # Testing if player A can block
                return True


def pitDetermination(board):
    neededValues = [0, 0, 0, 0, 0, 0]
    for i in range(6):
        if finalStore(board, i):     # 1. Putting the final seed in the player store
            neededValues.insert(i, board[1][i])
            continue
        elif blockOpp(board, i):    # 2. Block the opponent from putting a seed in there store
            neededValues.insert(i, board[1][i])
            continue
        elif collectOpp(board, i):  # 3. Put the player seed in the opponents empty pit
            neededValues.insert(i, board[1][i])
            continue
        # Consider eliminating
        #  elif canCollect(board, i) == True:  # 4. Empty the player pit
            #  print("Move the seeds in pit", 6-i, "to empty your pit")

    moveRecommendation = {
        "pit1A": neededValues[5],
        "pit2A": neededValues[4],
        "pit3A": neededValues[3],
        "pit4A": neededValues[2],
        "pit5A": neededValues[1],
        "pit6A": neededValues[0],
    }

    return moveRecommendation


# Printing the randomized Mancala board
print(' ', *board[0][1:7])
print(board[0][0], '            ', board[1][6])
print(' ', *board[1][0:6])

print(pitDetermination(board))
