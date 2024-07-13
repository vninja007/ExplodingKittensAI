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
    def getMove(self, toDraw):
        #Return None = draw ONE card
        psbls = whatcaniplay(self.hand)+[None]
        random.shuffle(psbls)
        if(psbls[0]):
            self.hand.remove(psbls[0])
            if(psbls[0][0]=='C'):
                self.hand.remove(psbls[0])
        return psbls[0]
    def cardDrawn(self,card):
        if(card=='EXPL'):
            if('DEF' not in self.hand):
                return 0
            else:
                self.hand.remove('DEF')
                return 1
        else:
            self.hand.append(card)
            return 2
    def getFavored(self):
        return self.hand.pop(random.randrange(len(self.hand)))

    
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
victim = 1
toDraw = 1
# while len(players):

print(players[0].hand)
move = 'skibidi'
while not turn:
    move = players[0].getMove(1)
    print(move)
    print(players[0].hand)

    if(not move):
        safe = players[turn].cardDrawn(deck.pop())
        if(not safe): players.pop(turn)
        if(safe==1): deck.insert(random.randrange(len(deck)),'EXP')
        turn += 1
    elif(move=='ATK'):
        toDraw = 2
        turn += 1; turn %= PLAYERS
    elif(move=='SKIP'):
        turn += 1; turn %= PLAYERS
    elif(move=='SHUF'):
        random.shuffle(deck)
    elif(move=='FVR'):
        players[turn].hand.append((fvrcard:=players[victim].getFavored()))
        print('favor got', fvrcard)
    elif(move=='STF'):
        players[turn].inform(turn,'STF',deck[:-4:-1])
    elif(move[0]=='C'):
        random.shuffle(players[victim].hand)
        players[turn].hand.append((cccard:=players[victim].hand.pop()))
        print('catcard got', cccard)
    


print(players[0].hand)




pass

# print(players[0].getMove())
print(time.time()-ctic)