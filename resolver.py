# Resolver file to play one round, small module functions per step/ action
from board import buildBoard

# set the board
Board = buildBoard()

# Set the player to the first player spot
def PlayerSet(Board):
    playerRow = Board[0]
    return playerRow # returns list of payer pits, ie: [store, 1,2,3,4,5,6]

# Determine gems in pit
def GemsinPit(Board, Row, Col):
    for Row in Board:
        for Col in Row:
            return Board[Row][Col]

# Detect if pit is empty
def PitisEmpty(Board, Row, Col):
    if GemsinPit(Board,Row,Col)== 0:
        return True
    else:
        return False

# Detect if opposite pit is empty
def oppEmpty(Board, Col):
    playerRow = PlayerSet(Board)
    oppRow = playerRow+1 # this is for possible changes, as opposed to just putting 1, more flexible
    if PitisEmpty(Board,oppRow,Col) == True:
        return True
    else: 
        return False

# If the player can collect, return true
def CanCollect(Board,Col,Row):
    # If the pit is empty and the opposite is not, return true
    if (PitisEmpty(Board,Col,Row)==True) and (oppEmpty(Board,Col)==False):
        return True
    else:
        return False

# Function to determine if the final piece lands in the player store
def finalStore(board, player,n):
    gemsHand = board[player][n]
    point = n
    if (gemsHand>1) and (point != -1):
        if player == 0:
            point-=1
            board[player][point] +=1
            gemsHand-=1
        if player == 1:
            point +=1
            board[player][point] +=1
            gemsHand-=1
    
    elif (gemsHand>1) and((player == 1 and point == -1) or (player==0 and point == 0)):
        if player == 1:
            board[player][point]+=1
            gemsHand-=1
            player-=1
        else:
            player+=1
            board[player][point]+=1
            gemsHand-=1
    elif (gemsHand == 1) and ((player == 1 and point == -1) or (player == 0 and point ==0)):
        if player==1:
            gemsHand-=1
            return True
        else:
            gemsHand-=1
            return True
    else:
        return False

# function to determin if opponent can be blocked      
#def blockOpp(board): -> Return Boolean

# function to determin where last seed lands 
# def landingPlaceRow -> Returns Row
# def LandingPlaceCol -> Returns Col

def pitDetermination(board, player):
    #1. Putting the final seed in the player store
    #2. Block the opponent from putting a seed in there store
    #3. Put the player seed in the opponents empty pit
    #4. Empty the player pit
    #5. If all else fails, play the righmost pit.

    row = landingPlaceRow(Board,player)
    col = landingPlaceCol(Board,player)

    for player in board:
        for n in player:
            if finalStore(board,n) == True:
                return n
            elif blockOpp(board, n) == True:
                return n 
            elif (row == 1) and (PitisEmpty(board, row, col) == True):
                return n
            elif CanCollect(Board,n,row) == True:
                return n
        else:
            return 6

def UserChoice():
    # in traditional set up, 48 stones are used. ie 24 per player, 6 per pit
    playInput = print("Player 1, it is suggested you grab from pit", pitDetermination(Board))