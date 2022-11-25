from pickle import TRUE
from sqlite3 import Row
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# Encoding that will store all of your constraints
E = Encoding()

# Creative Variables
GEMS = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24} # Note: we should probably add a limit of 24 gems
ROW = {1,2}
COLUMN = {0,1,2,3,4,5,6}
PIT = [ROW,COLUMN]
COLLECTS = TRUE
OPPOSITE = TRUE


PROPOSITIONS = []


# Proposition to check the position of the hand and how many gem it has
@proposition(E)
class HandProposition:
    def __init__(self, gems, pit):
        self.gems = gems
        self.pit = pit

    def __repr__(self):
        return f"{self.gems}@{self.pit}"

for pit in PIT:
    for row in ROW:
        for column in COLUMN:
            PROPOSITIONS.append(HandProposition(pit,row))

# Proposition to check which pit is selected
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
# Note: This is an array of gems taken from input. The index goes like this: pit a6 ... pit a0, pit b6 ... pit b0
b = []
# Variables of the hand
r = 0
c = 0
g = b[14 - 7 * (r - 1) - c - 1]
# Variable of the player
p = 0
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
    # Simulate grabbing all of the gems in a pit
    E.add_constraint(SelectPit(r,c) >> PitProposition(r, c, 0) & HandProposition(r,c,g))
    # Simulate dropping of the gems (Comment: I just realize theres gonna a bug when a pit with 15 or more gems is selected rendering an unsatifiable board, I attempted to fix it, but who knows)
    while (g != 0):
        if r == (1 + p) and c == 0:
            E.add_constraint(HandProposition(r,c,g) >> HandProposition(2-p,6,g-1) & PitProposition(2,6,b[6 + 7 * p]+1) & ~PitProposition(2,6,b[6+7*p]))
            r = 2 - p
            c = 6
            b[6 + 7*p] = b[6 + 7*p]+1
        if r == (2 - p) and c == 1:
            E.add_constraint(HandProposition(r,c,g) >> HandProposition(1+p,6,g-1) & PitProposition(1+p,6,b[0 + 7*p]+1) & ~PitProposition(1+p,6,b[0 + 7*p]))
            r = 1 + p
            c = 6
            b[0 + 7*p] = b[0 + 7*p]+1
        else:
            E.add_constraint(HandProposition(r,c,g) >> HandProposition(r,c-1,g-1) & PitProposition(r,c-1,b[14 - 7 * (r - 1) - c - 1] + 1) & ~PitProposition(r,c-1,b[14 - 7 * (r - 1) - c - 1]))
            c = c - 1
            b[14 - 7 * (r - 1) - c - 1] = b[14 - 7 * (r - 1) - c - 1] + 1
        g = g - 1

    # Simulate the game rule: if the final seed lands on the player's store, that person may get another turn.
    for gems in GEMS:
        E.add_constraint(HandProposition(p+1,0,gems) >> A)
    # Simulate the game rule: if the final seed lands on an empty pit, the player collects gems from opposite pits.
    if c != 0:
        E.add_constraint(HandProposition(r,c,0) & PitProposition(r,c,1) >> C)

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