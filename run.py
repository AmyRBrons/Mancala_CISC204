from pickle import TRUE
from sqlite3 import Row
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from board import buildBoard
import copy

# Encoding that will store all of your constraints
E = Encoding()

# Creative Variables
GEMS = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24}
ROW = {0,1}
COLUMN = {0,1,2,3,4,5,6}

"""
How it works: The logic has a bunch of propositions and constraints which are defined by the game. The propositions
represent various things within the game. The constraints represent the physical and spoken rules of the game. For use of application,
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

# Proposition to check which pit is selected
@constraint.exactly_one(E)
@proposition(E)
class SelectPit:
    def __init__(self, row, column):
        self.row = row
        self.column = column
    
    def __repr__(self):
        return f"selected-{self.column}"

# Proposition of the pit and how many gems it contains
@proposition(E)
class PitProposition:
    def __init__(self, row, column, gems):
        self.row = row
        self.column = column
        self.gems = gems
    
    def __repr__(self):
        return f"{self.row}@{self.column}={self.gems}"

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

# Board randomizer
# Note: This is a 2d array which overlay the position. It goes like this:[[a0,a1,a2,a3,a4,a5,a6][b1,b2,b3,b4,b5,b6]] or b[r][c]
originalGemList = buildBoard()
print(originalGemList)
#TESTING BLOCK STARTS

"""
#TEST 1: Strategy 1 - Should return true
originalGemList = [[0, 1, 3, 4, 8, 9, 10],
             [0, 0, 0, 0, 0, 0, 0]]
print(originalGemList)
"""

"""
#TEST2: Should return false
originalGemList = [[0, 0, 2, 0, 0, 0, 0],
             [0, 4, 4, 4, 4, 4, 4]]
print(originalGemList)
"""

"""
#TEST3: RANDOM BOARD - Should return false
originalGemList = [[0, 21, 3, 0, 0, 0, 0], [19, 0, 3, 1, 0, 1, 0]]
print(originalGemList)
"""
#TESTING BLOCK ENDS

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
        if column != 0 and originalGemList[0][column]!=0:
            # Ensure we can't select an empty pit
            E.add_constraint(SelectPit(0, column) >>(~PitProposition(0, column, 0)))
            # Calculating the final board state
            newGemList = copy.deepcopy(originalGemList)
            finalRow = 0
            finalColumn = column
            gemCount = originalGemList[finalRow][finalColumn]
            newGemList[finalRow][finalColumn] = 0
            while gemCount != 0:
                # Move the hand to the opponent's row after dropping a gem in the bank
                if finalColumn == 0 and finalRow == 0:
                    finalColumn = 6
                    if finalRow == 0:
                        finalRow = 1
                    else:
                        finalRow = 0
                # Skip the opponent bank
                elif finalColumn == 1 and finalRow != 0:
                    finalColumn = 6
                    finalRow = 0
                else:
                    finalColumn = finalColumn - 1
                newGemList[finalRow][finalColumn] = newGemList[finalRow][finalColumn] + 1
                gemCount = gemCount - 1
            # Put the final state of the board in the logic.
            for PitRow in ROW:
                for PitColumn in COLUMN:
                    E.add_constraint(SelectPit(0, column) >> PitProposition(PitRow, PitColumn, newGemList[PitRow][PitColumn]))
            E.add_constraint(SelectPit(0,column) >> FinalSeed(finalRow,finalColumn))

    # Simulate the game rule: if the final seed lands on the player's store, that person may get another turn.
    E.add_constraint(FinalSeed(0, 0) >> PlayerTurnNext())
    # Simulate the game rule: if the final seed lands on an empty pit, the player collects gems from opposite pits.
    for row in ROW:
        for column in COLUMN:
            if column != 0:
                E.add_constraint((FinalSeed(row,column) & PitProposition(row,column,1)) >> PlayerCollects())

    """
    Configuration related-constraints
    """
    # Blocking (Uncomment so the logic would check to see if its possible to prevent the opponent from getting another turn)
    """
    for column in COLUMN:
        if column != 0:
            E.add_constraint(~PitProposition(1,column,column))
    """
    
    # Check for next turn (Uncomment so the logic would check to see if its possible to get another turn)
    # E.add_constraint(FinalSeed(0,0))

    # Check for collection (Uncomment so the logic would check to see if its possible to collect gems)
    # E.add_constraint(PlayerCollects())
    return E

if __name__ == "__main__":

    T = constraints()
    T = T.compile()
    print("\nSatisfiable: %s" % T.satisfiable())
    """
    sol = T.solve()
    E.pprint(T, sol)
    E.introspect(sol)
    print_theory(sol)
    
"""
    # Supposed to print out the likeihood of the selected pits
    # for v,vn in zip([S1,S2,S3,S4,S5,S6], '123456'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        # print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
