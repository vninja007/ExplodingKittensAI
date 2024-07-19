import random
from players import *
import time; ctic = time.time()





def initDeck(deck, playerdecks, players, PLAYERS):
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

    players.append(ARPlayer(str(0),playerdecks[0]))
    random.shuffle(players[-1].hand)
    players.append(ARPlayer(str(1),playerdecks[1]))
    random.shuffle(players[-1].hand)


    # players.append(CommonSensePlayer(str(0),playerdecks[0]))
    # random.shuffle(players[-1].hand)
    # players.append(Player(str(1),playerdecks[1]))
    # random.shuffle(players[-1].hand)


    # random.shuffle(players)

    # for player in range(PLAYERS):
    #     players.append(Player(str(player),playerdecks[player]))
    #     random.shuffle(players[-1].hand)


# while len(players):


def simulateGame(PLAYERS):
    deck = []
    playerdecks = [[('DEF')] for n in range(PLAYERS)] #0 = me, 1+ = AIs
    players = []
    initDeck(deck, playerdecks, players, PLAYERS)
    turn = 0
    turnctr = 0 # Number of cards drawn from deck
    movectr = 0 # Number of ATK + SKIP + Cards Drawn
    victim = 1
    toDraw = 1
    while toDraw and len(players)>1:
        move = 'skibidi'
        while move:
            move = players[turn].getMove(toDraw, movectr, turnctr, [len(i) for i in playerdecks])
            if(move):
                playerdecks[turn].remove(move)
                if(move[0]=='C'):
                    playerdecks[turn].remove(move)
            victim = turn^1
            if(not move): continue
            for player in players:
                player.inform(turn, move, victim if move=='FVR' or move[0]=='C' else None)

            if(move=='ATK'):
                toDraw = toDraw+1 if toDraw==1 else toDraw+2
                turn += 1; turn %= PLAYERS
                turnctr += 1
                movectr += 1
            elif(move=='SKIP'):
                turn += 1; turn %= PLAYERS
                turnctr += 1
                movectr += 1
            elif(move=='SHUF'):
                random.shuffle(deck)
            elif(move=='FVR'):
                favorcard = players[victim].getFavored()
                # print('favorcard', favorcard)
                players[turn].hand.append(favorcard)
            elif(move=='STF'):
                players[turn].inform(turn,'STF',deck[:-4:-1])
            elif(move[0]=='C'):
                cardtaken = random.choice(players[victim].hand)
                players[victim].hand.remove(cardtaken)
                players[turn].hand.append(cardtaken)
                # print('cardtaken', cardtaken)
        safe = players[turn].cardDrawn(deck.pop())
        movectr += 1
        if(not safe): players.pop(turn); toDraw = 1
        else:
            if(safe==1): 
                if(not deck): deck = ['EXPL']
                else:
                    deck.insert(random.randrange(len(deck)),'EXPL')
            toDraw -= 1
            if(toDraw == 0): turn += 1; turn %= PLAYERS; toDraw = 1; turnctr += 1
    return players[0].name

# print(players[0].hand)
# print("Player",players[0].name,"won by",players[0].hand.count('DEF'),'defuses')
# print(players[0].getMove())

onewin = 0
zerowin = 0
for _ in range(int(1e4)):
    res = simulateGame(2)
    if(res=='1'): onewin += 1
    else: zerowin += 1

print(zerowin, onewin, onewin/(onewin+zerowin))
print(time.time()-ctic)