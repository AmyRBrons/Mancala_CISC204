from pickle import TRUE
from sqlite3 import Row
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from board import buildBoard

#from resolver import NextTurn as Next

# Encoding that will store all of your constraints
E = Encoding()

#from resolver import NextTurn as Next


# Creative Variables
GEMS = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24} # Note: we should probably add a limit of 24 gems
ROW = {0,1}
COLUMN = {0,1,2,3,4,5,6}
PIT = [COLUMN,COLUMN]
COLLECTS = TRUE
OPPOSITE = TRUE


PROPOSITIONS = []

"""
Just a reminder on how it works: The logic has a bunch of propositions and constraints which are not defined. The propositions
represent various things. The constraint represent the physical and spoken rules of the game. For use of application,
the various propositions must be forced true using external file or hard-coding it and it should run to check if there
is a solution.
"""


# Proposition to check the position of the final seed
@constraint.exactly_one(E)
@proposition(E)
class FinalSeed:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __repr__(self):
        return f"{self.row}@{self.column}"

for row in ROW:
    for column in COLUMN:
        PROPOSITIONS.append(FinalSeed(row,column))

# Proposition to check which pit is selected
@constraint.exactly_one(E)
@proposition(E)
class SelectPit:
    def __init__(self, row, column):
        self.row = row
        self.column = column
    
    def __repr__(self):
        return f"selected-{self.column}"

for column in COLUMN:
    if column != 0:
        PROPOSITIONS.append(SelectPit(0, column))

# Proposition of the pit and how many gems it contains
@proposition(E)
class PitProposition:
    def __init__(self, row, column, gems):
        self.row = row
        self.column = column
        self.gems = gems
    
    def __repr__(self):
        return f"{self.row}@{self.column}={self.gems}"

for row in ROW:
    for column in COLUMN:
        for gems in GEMS:
            PROPOSITIONS.append(PitProposition(row, column, gems))

# Propositon to identify which player gets another turn
@proposition(E)
class PlayerTurnNext:
    def __init__(self):
        self = self
    def __repr__(self):
        return f"A"


# Proposition to determine if the player collects gems
@proposition(E)
class PlayerCollects:
    def __init__(self):
        pass

    def __repr__(self):
        return f"C"

# Propositon to determine if the two pits are opposite   
@proposition(E)
class OppositePits:
    def __init__(self, row, column, opposite):
        self.row = row
        self.column = column
        self.opposite = opposite
    
    def __repr__(self):
        return f"{self.column}@{self.row+1}={7 - self.column}@{self.row}={self.opposite}"

for row in ROW:
    for column in COLUMN:
        opposite = OPPOSITE
        PROPOSITIONS.append(OppositePits(row, column, opposite))

# Call your variables whatever you want
# Note: This is a 2d array which overlay the position. It goes like this:[[a0,a1,a2,a3,a4,a5,a6][b1,b2,b3,b4,b5,b6]] or b[r][c]
originalGemList = buildBoard()
print(originalGemList)
# Variables of the hand
finalRow = 0
finalColumn = 0
gemCount = 0
# Variable of the player
player = 0
# Selection variables (Expermentational, let's try if we can uses likeilhoods function to get our result)
'''
S1 = SelectPit(0, 1)
S2 = SelectPit(0, 2)
S3 = SelectPit(0, 3)
S4 = SelectPit(0, 4)
S5 = SelectPit(0, 5)
S6 = SelectPit(0, 6)
'''

def constraints():
    """
    All of the board related constraints.
    """
    # Pit can only have a fixed number of gems.
    for row in ROW:
        for column in COLUMN:
            constraint.add_exactly_one(E, [PitProposition(row, column, 0), PitProposition(row, column, 1), PitProposition(row, column, 2), PitProposition(row, column, 3), PitProposition(row, column, 4), PitProposition(row, column, 5), PitProposition(row, column, 6), PitProposition(row, column, 7), PitProposition(row, column, 8), PitProposition(row, column, 9), PitProposition(row, column, 10), PitProposition(row, column, 11), PitProposition(row, column, 12), PitProposition(row, column, 13), PitProposition(row, column, 14), PitProposition(row, column, 15), PitProposition(row, column, 16), PitProposition(row, column, 17), PitProposition(row, column, 18), PitProposition(row, column, 19), PitProposition(row, column, 20), PitProposition(row, column, 21), PitProposition(row, column, 22), PitProposition(row, column, 23), PitProposition(row, column, 24)])

    """
    All of the game related constraints.
    """
    # Simulate what happens if you select a pit
    for column in COLUMN:
        if column != 0:
            # Ensure we can't select an empty pit
            E.add_constraint(SelectPit(0, column) & ~PitProposition(0, column, 0))
            newGemList = originalGemList.copy()
            finalRow = player
            finalColumn = column
            gemCount = originalGemList[finalRow][finalColumn]
            newGemList[finalRow][finalColumn] = 0
            while gemCount != 0:
                # Move the hand to the opponent's row after dropping a gem in the bank
                if finalColumn == 0 and finalRow == player:
                    finalColumn = 6
                    if player == 0:
                        finalRow = 1
                    else:
                        finalRow = 0
                # Skip the opponent bank
                elif finalColumn == 1 and finalRow != player:
                    finalColumn = 6
                    finalRow = player
                else:
                    finalColumn = finalColumn - 1
                newGemList[finalRow][finalColumn] = newGemList[finalRow][finalColumn] + 1
                gemCount = gemCount - 1
            # Put the final state of the board in the logic.
            for PitRow in ROW:
                for PitColumn in COLUMN:
                    E.add_constraint(SelectPit(player, column) >> PitProposition(PitRow, PitColumn, newGemList[PitRow][PitColumn]))

    # Simulate the game rule: if the final seed lands on the player's store, that person may get another turn.
    E.add_constraint(FinalSeed(player, 0) >> PlayerTurnNext())
    # Simulate the game rule: if the final seed lands on an empty pit, the player collects gems from opposite pits.
    for row in ROW:
        for column in COLUMN:
            if column != 0:
                E.add_constraint((FinalSeed(row,column) & PitProposition(row,column,1)) >> PlayerCollects())
    """
    Configuration related-constraints
    """

    # If we want to enable blocking
    '''
    for column in COLUMN:
        if column != 0:
            E.add_constraint(~PitProposition(1,column,column))
    '''
    # Check for next turn
    # E.add_constraint(FinalSeed(0,0) >> PlayerTurnNext())

    # Check for collection
    '''
    for row in ROW
        for column in COLUMN:
            E.add_constraint((FinalSeed(row, column) & PitProposition(row, column, 1)) >> PlayerTurnNext())
    '''



if __name__ == "__main__":

    T = constraints()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    # Debugging based on forum suggestion
    '''
    sol = T.solve()
    E.pprint(T, sol)
    E.introspect(sol)
    print_theory(sol)
    '''

    # Debugging based on a experimental suggestion
    '''
    for v,vn in zip([S1,S2,S3,S4,S5,S6], '123456'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()

    '''
