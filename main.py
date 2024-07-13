import random
import time; ctic = time.time()


deck = []
PLAYERS = 2

class Card:
    def __init__(self, type):
        self.type = type
    def __str__(self):
        return self.type
    def __repr__(self):
        return self.type

class Player:
    def __init__(self, hand):
        self.hand = hand
    def inform(self, player, move, moveData):
        pass
    def getMove(self):
        psbls = whatcaniplay(self.hand)
        hand.remove(psbls[0])
        return psbls[0]


playerdecks = [[Card('DEF')] for n in range(PLAYERS)] #0 = me, 1+ = AIs



deck.extend([Card('ATK') for i in range(4)])
deck.extend([Card('SKIP') for i in range(4)])
deck.extend([Card('SHUF') for i in range(4)])
deck.extend([Card('FVR') for i in range(4)])
deck.extend([Card('STF') for i in range(5)])
deck.extend([Card('NOPE') for i in range(5)])

deck.extend([Card('C1') for i in range(4)])
deck.extend([Card('C2') for i in range(4)])
deck.extend([Card('C3') for i in range(4)])
deck.extend([Card('C4') for i in range(4)])
deck.extend([Card('C5') for i in range(4)])


random.shuffle(deck)

for player in playerdecks:
    for i in range(7):
        player.append(deck.pop())


deck.extend([Card('DEF') for i in range(1+(PLAYERS<5))])
deck.extend([Card('EXPL') for i in range(PLAYERS-1)])
random.shuffle(deck)

players = []
for player in range(PLAYERS):
    players.append(Player(playerdecks[player]))

print(players)




def whatcaniplay(deck):
    possible = []
    playerdeck = [str(card) for card in deck]
    mapping = {card:{idx for idx in range(len(playerdeck)) if card==playerdeck[idx]} for card in playerdeck}
    print(playerdeck)
    print(mapping)
    
    if('ATK' in mapping): possible += ['ATK']*len(mapping['ATK']) 
    if('SKIP' in mapping): possible += ['SKIP']*len(mapping['SKIP']) 
    if('SHUF' in mapping): possible += ['SHUF']*len(mapping['SHUF']) 
    if('FVR' in mapping): possible += ['FVR']*len(mapping['FVR']) 
    if('STF' in mapping): possible += ['STF']*len(mapping['STF']) 
    if('C1' in mapping): possible += ['C1']*(len(mapping['C1'])//2)
    if('C2' in mapping): possible += ['C2']*(len(mapping['C2'])//2)
    if('C3' in mapping): possible += ['C3']*(len(mapping['C3'])//2)
    if('C4' in mapping): possible += ['C4']*(len(mapping['C4'])//2)
    if('C5' in mapping): possible += ['C5']*(len(mapping['C5'])//2)
    
    
    # if()
    print(possible)

print(time.time()-ctic)