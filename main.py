import random
import time; ctic = time.time()


deck = []
PLAYERS = 2

class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand
    def inform(self, player, move, moveData):
        pass
    def getMove(self):
        #Return None = draw ONE card
        psbls = whatcaniplay(self.hand)+[None]
        self.hand.remove(psbls[0])
        return psbls[0]
    def cardDrawn(self):
        pass
    
def whatcaniplay(deck):
    possible = []
    playerdeck = [str(card) for card in deck]
    mapping = {card:{idx for idx in range(len(playerdeck)) if card==playerdeck[idx]} for card in playerdeck}
    
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
    return possible

def initDeck():
    deck.extend([('ATK') for i in range(4)])
    deck.extend([('SKIP') for i in range(4)])
    deck.extend([('SHUF') for i in range(4)])
    deck.extend([('FVR') for i in range(4)])
    deck.extend([('STF') for i in range(5)])
    deck.extend([('NOPE') for i in range(5)])

    deck.extend([('C1') for i in range(4)])
    deck.extend([('C2') for i in range(4)])
    deck.extend([('C3') for i in range(4)])
    deck.extend([('C4') for i in range(4)])
    deck.extend([('C5') for i in range(4)])


    random.shuffle(deck)

    for player in playerdecks:
        for i in range(7):
            player.append(deck.pop())


    deck.extend([('DEF') for i in range(1+(PLAYERS<5))])
    deck.extend([('EXPL') for i in range(PLAYERS-1)])
    random.shuffle(deck)

    for player in range(PLAYERS):
        players.append(Player(str(player),playerdecks[player]))
        random.shuffle(players[-1].hand)



playerdecks = [[('DEF')] for n in range(PLAYERS)] #0 = me, 1+ = AIs
players = []
initDeck()

turn = 0
# while len(players):
#     pass

print(players[0].getMove())
print(time.time()-ctic)