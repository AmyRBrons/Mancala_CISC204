import random
#Sample of user input building script

def buildBoard():
    player =0
    player1store = 0
    player2store = 0
    
    pit1 = int(input('Please enter the number of gems in pit 1 (please note you only have 24 gems to split bewteen these 6 pits.)'))
    Board[player][1] = pit1
    pit2 = int(input('Please enter the number of gems in pit 2 (please note you only have', 24-pit1,'gems left)'))
    Board[player][2] = pit2
    pit3 = int(input('Please enter the number of gems in pit 3 (please note you only have', 24-pit1-pit2, 'gems left)'))
    Board[player][1] = pit3
    pit4 = int(input('Please enter the number of gems in pit 4 (please note you only have', 24-pit1-pit2-pit3,'gems left)'))
    Board[player][2] = pit4
    pit5 = int(input('Please enter the number of gems in pit 5 (please note you only have', 24-pit1-pit2-pit3-pit4, 'gems left)'))
    Board[player][2] = pit5
    pit6 = int(input('Please enter the number of gems in pit 6 (please note you only have', 24-pit1-pit2-pit3-pit4, 'gems left)'))
    Board[player][1] = pit6

    player21 = random.randint(0,24)
    player22range = 24 - player21
    player22 = random.randint(0,player22range)
    player23range = player22range-player22
    player23 = random.randint(0,player23range)
    player24range = player23range - player23
    player24 = random.randint(0,player24range)
    player25range = player24range - player24
    player25 = random.randint(0, player25range)
    player26 = player25range - player25
    

    Board = [[player1store,pit1,pit2,pit3,pit4,pit5,pit6],[player21,player22,player23,player24,player25range,player26,player2store]]
    return Board

def PlayerSet(Board):
    playerRow = Board[0]
    return playerRow

def GemsinPit(Board, Row, Col):
    for Row in Board:
        for Col in Row:
            return Board[Row][Col]
    
def PitisEmpty(Board, Row, Col):
    if GemsinPit(Board,Row,Col)== 0:
        return True
    else:
        return False

def oppEmpty(Board, Col):
    playerRow = PlayerSet(Board)
    oppRow = playerRow+1
    if PitisEmpty(Board,oppRow,Col) == True:
        return True
    else: 
        return False

def CanCollect(Board,Col,Row):
    if (PitisEmpty(Board,Col,Row)==False) and (oppEmpty(Board,Col)==False):
        return True
    else:
        return False

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

        
#def blockOpp(board):



def pitDetermination(board, player):
    #1. Putting the final seed in the player store
    #2. Block the opponent from putting a seed in there store
    #3. Put the player seed in the opponents empty pit
    #4. Empty the player pit
    #5. If all else fails, play the righmost pit.
    for player in board:
        for n in player:
            if finalStore(board,n) == True:
                return n
            elif blockOpp(board, n) == True:
                return n 
            elif oppEmpty(board, n) == True:
                return n
            elif emptyPit(board, n) == True:
                return n
        else:
            return 4

def UserChoice():
    # in traditional set up, 48 stones are used. ie 24 per player, 6 per pit
    playInput = print("Player 1, it is suggested you grab from pit", pitDetermination(Board))