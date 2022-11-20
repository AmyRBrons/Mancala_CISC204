
Board = [[0,6,6,6,6,6,6],
         [6,6,6,6,6,6,0]]

player1store = 0
player2store = 0

"""
Sample of user input building script

def buildBoard():
    player = int(input('Please enter the player number you want (1 or 2)'))
    player =-1
    
    if player == 0:
        pit1 = int(input('Please enter the number of gems in pit 1 (please note you only have 24 gems to split bewteen these 4 pits.)'))
        Board[player][1] = pit1
        pit2 = int(input('Please enter the number of gems in pit 2 (please note you only have', 24-pit1,'gems left)'))
        Board[player][2] = pit2
        pit3 = int(input('Please enter the number of gems in pit 3 (please note you only have 24 gems to split bewteen these 4 pits.)'))
        Board[player][1] = pit1
        pit1 = int(input('Please enter the number of gems in pit 4 (please note you only have 24 gems to split bewteen these 4 pits.)'))
        Board[player][1] = pit1"""

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

def oppEmpty(Board,player, pit):
    if player == 1:
        pit = pit -1
    else: 
        pit = pit+1
    opp = player+1
    if Board[opp][pit] == 0:
        return True
    else:
        return False

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