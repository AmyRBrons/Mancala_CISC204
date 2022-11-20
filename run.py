
from pickle import TRUE
from sqlite3 import Row
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# Encoding that will store all of your constraints
E = Encoding()

# Creative Variables
GEMS = {4}
Row = {1,2}
COLUMN = {1,2,3,4}
PIT = [Row,COLUMN]
COLLECTS = TRUE
OPPOSITE = TRUE


PROPOSITIONS = []


# Proposition to check if gems are in particular pit
@proposition(E)
class AmountOfGems:
    def __init__(self, gems, pit):
        self.gems = gems
        self.pit = pit

    def __repr__(self):
        return f"{self.gems}@{self.pit}"

for pit in PIT:
    for row in Row:
        for column in COLUMN:
            PROPOSITIONS.append(AmountOfGems(pit,row))

# Proposition to check if the pit is on the players side
@proposition(E)
class SideOfPit:
    def __init__(self, row, pit):
        self.row = row
        self.pit = pit
    
    def __repr__(self):
        return f"{self.pit}={self.row}"

for pit in PIT:
    for row in Row:
        for column in COLUMN:
            PROPOSITIONS.append(SideOfPit(pit,row))

# Proposition of the pit and how mant gems it contains
@proposition(E)
class PitProposition:
    def __init__(self, pit, gems):
        self.gems = gems
        self.pit = pit
    
    def __repr__(self):
        return f"{self.gems}@{self.pit}"

for pit in PIT:
    for row in Row:
        for column in COLUMN:
            PROPOSITIONS.append(PitProposition(pit,row))

# Propositon to identify which player gets another turn
@proposition(E)
class PlayerTurnNext:
    def __init__(self):
        self = self
    def __repr__(self):
        return f"{self}"

for pit in PIT:
    for row in Row:
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
    for row in Row:
        for column in COLUMN:
            PROPOSITIONS.append(PlayerCollects(pit,row))

# Propositon to determine if the two pits are opposite   
@proposition(E)
class OppositePits:
    def __init__(self, row, column, gems, opposite):
        self.opposite = opposite
        self.row = row
        self.column = column
        self.gems = gems
    
    def __repr__(self):
        return f"{self.colum}@{self.row+1}={self.column}@{self.row}={self.opposite}"

for pit in PIT:
    for row in Row:
        for column in COLUMN:
            for gems in GEMS:
                PROPOSITIONS.append(OppositePits(pit,row,column,gems))


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
h = BasicPropositions("h")
s = BasicPropositions("s")   
p = BasicPropositions("p")
t = BasicPropositions("t")
c = BasicPropositions("c")
# At least one of these will be true
x = FancyPropositions("x")
y = FancyPropositions("y")
z = FancyPropositions("z")



def constraints():
    # Player A can only move gems on their side of the board
    E.add_constraint(h & s >> p)
    # Player A cannot drop a gem in Player B's store
    E.add_constraint(h >> ~ s)
    # A pocket must have seeds in it
    E.add_constraint(p >> h)
    # Dropping a gem in a pit
    E.add_constraint(h >> h & p)
    # If the final seed is in player A's store, then player A gets
    # another turn
    E.add_constraint(h >> t)
    # Player A collects seeds from Player B's pit if the last seed
    # is dropped in the opposite pit
    E.add_constraint((h & ~p) & s >> c)

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
    for v,vn in zip([h,s,p,x,y,z], 'hspxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        #print(" %s: %.2f" % (vn, likelihood(T, v)))
        print(" %s: %f" % (vn, likelihood(T, v)))
    print()
