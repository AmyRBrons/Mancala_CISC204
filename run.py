from pickle import TRUE
from sqlite3 import Row
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from board import buildBoard
from resolver import PitisEmpty as Empty
from resolver import GemsinPit as Gems
from resolver import CanCollect as Collect
from resolver import NextTurn as Next

# Encoding that will store all of your constraints
E = Encoding()

# Creative Variables
GEMS = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24} # Note: we should probably add a limit of 24 gems
ROW = {0,1}
COLUMN = {0,1,2,3,4,5,6}
PIT = [COLUMN,COLUMN]
COLLECTS = TRUE
OPPOSITE = TRUE


PROPOSITIONS = []


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

for row in ROW:
    for column in COLUMN:
        PROPOSITIONS.append(SelectPit(row, column))

# Proposition of the pit and how many gems it contains
@proposition(E)
class PitProposition:
    def __init__(self, row, column, gems):
        self.pit = pit
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
        return f"{self}"

for pit in PIT:
    for row in ROW:
        for column in COLUMN:
            PROPOSITIONS.append(PlayerTurnNext())


# Proposition to determine if the player collects gems
@proposition(E)
class PlayerCollects:
    def __init__(self, collects, gems):
        self.collects = collects
        self.gems = gems

    def __repr__(self):
        return f"{self.collects}={self.gems!=0}"

for pit in PIT:
    for row in ROW:
        for column in COLUMN:
            PROPOSITIONS.append(PlayerCollects(pit,row))

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


# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class BasicPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"


# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html
@constraint.at_least_one(E)
@proposition(E)
class FancyPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"

# Call your variables whatever you want
# Note: This is a 2d array which overlay the position. It goes like this:[[a0,a1,a2,a3,a4,a5,a6][b1,b2,b3,b4,b5,b6]] or b[r][c]
originalGemList = buildBoard()
# Variables of the hand
finalRow = 0
finalColumn = 0
gemCount = 0
# Variable of the player
player = 0
# Special Outcomes
A = PlayerTurnNext()
C = PlayerCollects()

def constraints():
    """
    All of the board related constraints.
    """
    # Pit can only have a fixed number of gems.
    for row in ROW:
        for column in COLUMN:
            constraint.add_exactly_one(E, [PitProposition(row, column, gems) for gems in GEMS])
    # Check which pit is opposite to each other (Comment: I have no idea for any good application, so maybe when its appropriate, I will figure out the constraint)
    # E.add_constraint(E, OppositePits())

    """
    All of the game related constraints.
    """
    # Simulate what happens if you select a pit
    for column in COLUMN:
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
        Pit = []
        # Put the final state of the board in the logic.
        for PitRow in ROW:
            for PitColumn in COLUMN:
                Pit.append(PitProposition(PitRow,PitColumn,newGemList[PitRow][PitColumn]))
        constraint.add_implies_all(E, SelectPit(player, column), Pit)

    # Simulate the game rule: if the final seed lands on the player's store, that person may get another turn.
    E.add_constraint(FinalSeed(player, 0) >> A)
    # Simulate the game rule: if the final seed lands on an empty pit, the player collects gems from opposite pits.
    for row in ROW:
        for column in COLUMN:
            if column != 0:
                E.add_constraint(FinalSeed(row,column) & PitProposition(row,column,1) >> C)

    """
    Configuration related-constraints
    """
    # Pit related constraint
    PitConfig = {}
    for (row,column,gem) in PitConfig:
        E.add_constraint(PitProposition(row,column,gem))
        
    NotPitConfig = {}
    for (row,column,gem) in NotPitConfig:
        E.add_constraint(~PitProposition(row,column,gem))

    # Check for next turn
    NextTurn = True
    if (NextTurn):
        E.add_constraint(PlayerTurnNext())
    else:
        E.add_constraint(~PlayerTurnNext())

    # Check for collection
    CanCollect = True
    if (CanCollect):
        E.add_constraint(PlayerCollects())
    else:
        E.add_constraint(~PlayerCollects())

    return E


if __name__ == "__main__":

    T = constraints()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([], 'hspxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        #print(" %s: %.2f" % (vn, likelihood(T, v)))
        print(" %s: %f" % (vn, likelihood(T, v)))
    print()