# File to create board with gems based on user input
import random

# buildBoard function
def buildBoard():
    player = 0
    player1store = 0 # zero gems in the stores to start
    player2store = 0
    Board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
    # Give the user allowance to fill pits with stones
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

    #in progress
    # randomly fill player 2 gems
    player21 = random.randint(0,10)
    runningtot = 24-player21
    player22 = random.randint(0,player22range)
    player23range = player22range-player22
    player23 = random.randint(0,player23range)
    player24range = player23range - player23
    player24 = random.randint(0,player24range)
    player25range = player24range - player24
    player25 = random.randint(0, player25range)
    player26 = player25range - player25
    
    # set board
    Board = [[player1store,pit1,pit2,pit3,pit4,pit5,pit6],[player2store,player21,player22,player23,player24,player25range,player26]]
    return Board

