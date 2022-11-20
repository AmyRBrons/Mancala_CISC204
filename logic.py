
from pickle import TRUE
from sqlite3 import Row
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# Encoding that will store all of your constraints
E = Encoding()

# Creative Variables
GEMS = []#how many max stones
Player = [1,2]
Row = [1,2]
COLUMN = [1,2,3,4,5,6,7]
PIT = [Row, COLUMN]
COLLECTS = TRUE
OPPOSITE = TRUE
Player1banks = [1, 7]
Player2bank = [2,0]
Hand = range(48)

PROPOSITIONS = []

# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class BasicPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"

@proposition(E)
class pitGems:
    def __init__(self, Player, GEMS, pit):
        self.Player = Player
        self.GEMS = GEMS
        self.pit = pit
    
    def __repr__(self):
        return f"{self.Player}@{self.pit}={self.GEMS}"
for player in Player:
    for Pit in PIT:
        for gems in GEMS:
            PROPOSITIONS.append(pitGems(Player, GEMS, PIT))

# Propositon to identify the player
@proposition(E)
class PlayerTurn:
    def __init__(self, Player):
        self.Player = Player

    def __repr__(self):
        return f"{self.Player}"

for player in Player:
        PROPOSITIONS.append(PlayerTurn(Player))


# Proposition to the board
@proposition(E)
class Board:
    def __init__(self, rows, columns, pit):
        self.rows = rows
        self.columns = columns
        self.pit = pit

    def __repr__(self):
        return f"A{self.rows}@{self.columns}={self.pit}"

for row in Row:
    for column in COLUMN:
        for pit in PIT:
            PROPOSITIONS.append(Board(Row,COLUMN,PIT))
            E.add_constraint(PROPOSITIONS[-1])

# Propositon to determine if the pit is player 1 bank
@proposition(E)
class Bank1:
    def __init__(self, pit, player1bank):
        self.pit = pit
        self.player1bank = player1bank
    
    def __repr__(self):
        return f"A{self.pit}={self.player1bank}"

for pit in PIT:
    for player1bank in Player1banks:
        PROPOSITIONS.append(Bank1(PIT,Player1banks))

# Propositon to determine if the pit is player 1 bank
@proposition(E)
class Bank2:
    def __init__(self, pit, player2bank):
        self.pit = pit
        self.player2bank = player2bank
    
    def __repr__(self):
        return f"A{self.pit}={self.player2bank}"

for pit in PIT:
    for player2bank in Player2bank:
        PROPOSITIONS.append(Bank2(PIT,Player2bank))

class onPlayersSide:
    def __init__(self, player, pit, row):
        self.player = player
        self.pit = pit
        self.row = row
    
    def __repr__(self):
        return f"A{self.pit}@{self.row == self.player}"

for player in Player:
    for pit in PIT:
        for row in Row:
            PROPOSITIONS.append(onPlayersSide(Player, PIT, Row))

# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html

#@constraint.add_at_least_one(E)
@proposition(E)
class FancyPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"

@proposition(E)
class OppositePits:
    def __init__(self, row, column):
        self.row = row
        self.column = column
    def __repr__(self):
        return f"A{self.column}@{self.row} = {self.row+1}{self.column}"

for column in COLUMN:
    for row in Row:
        PROPOSITIONS.append(Board(Row,COLUMN,PIT))

#@constraint.none_of(E)
@proposition(E)
class PlayerDrops:
    def __init__(self, pit, player1bank, player2bank, hand):
        self.pit = pit
        self.player1bank = player1bank
        self.player2bank = player2bank
        self.hand = hand

    def __repr__(self):
        return f"A{self.hand !=0}and{self.pit!=self.player1bank} and{self.pit != self.player2bank}"

for pit in PIT:
    for player1bank in Player1banks:
        for player2bank in Player2bank:
            for hand in Hand:
                PROPOSITIONS.append(PlayerDrops(PIT, Player1banks, Player2bank, Hand ))

#@constraint.add_at_least_one(E)
@proposition
class PlayerPicks:
    def __init__(self, pit, player1bank, player2bank, gems, hand):
        self.pit = pit 
        self. player1bank = player1bank
        self.player2bank = player2bank
        self.gems = gems
        self.hand = hand

    def __repr__(self):
        return f"A{self.hand} += {self.gems}@{self.pit}if{self.pit != self.player1bank} and {self.pit != self.player2bank}"

for hand in Hand:
    for gems in GEMS:
        for pit in PIT:
            for player1bank in Player1banks:
                for player2bank in Player2bank:
                    PROPOSITIONS.append(PlayerPicks(PIT, Player1banks, Player2bank, GEMS, Hand))

#class GemsHand:"""

# Call your variables whatever you want
h = pitGems(Player,GEMS,PIT)
s = PlayerTurn(Player)   
p = Board(Row, COLUMN,PIT)
t = Bank1(PIT, Player1banks)
c = Bank2(PIT, Player2bank)
p = onPlayersSide(Player, PIT, Row)
# At least one of these will be true
x = OppositePits(Row, COLUMN)
y = PlayerDrops(PIT, Player1banks, Player2bank, Hand)
z = PlayerPicks(PIT, Player1banks, Player2bank, GEMS, Hand)



def constraints():
    # Player A can only move gems on their side of the board
    E.add_constraint(s >> p& ~t)
    # Player A cannot drop a gem in Player B's store
    E.add_constraint(y >> ~c)
    # A pocket must have seeds in it
    E.add_constraint(z >> h)
    # Dropping a gem in a pit
    E.add_constraint(y & ~c)
    # If the final seed is in player A's store, then player A gets
    # another turn
    E.add_constraint(y & t >> s)
    # Player A collects seeds from Player B's pit if the last seed
    # is dropped in the opposite pit
    E.add_constraint(y & x >> z & ~p)

    constraint.add_exactly_one(E, h,s,p)

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
