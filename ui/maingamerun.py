import random
from players import *
import time; ctic = time.time()

#Deck Structure
PLAYERS = 2# gui purposes :(

#[DEF, NOPE, ATK, SKIP, FVR, SHUF, STF, C1, C2, C3, C4, C5]
#[0.   1,    2,   3,    4,   5,    6,   7,  8,  9, 10, 11]

#EXPL = -1

def initDeck(deck, playerdecks, players, PLAYERS):
    rng.shuffle(deck)
    for player in playerdecks:
        for i in range(7):
            player[deck.pop()]+=1
    deck.extend([0 for i in range(1+(PLAYERS<5))])
    deck.extend([-1 for i in range(PLAYERS-1)])

    rng.shuffle(deck)
    players.append(CommonSensePlayer(0,playerdecks[0]))
    players.append(RunningPlayer(1,playerdecks[1]))

def simulateMove(move, players, turn, turnctr, movectr, victim, toDraw, deck):
    if(move):
        players[turn].numCards -= 1
        players[turn].hand[move] -= 1
        if(move>=7):
            players[turn].numCards -= 1
            players[turn].hand[move] -= 1
    victim = turn^1

    if(move==2):
        # if(turn==0 and players[1].hand[1]>0 and turnctr>25):
        #     players[1].hand[1] -= 1;
        #     players[1].numCards -= 1;
        # else:
            toDraw = toDraw+1 if toDraw==1 else toDraw+2
            turn += 1; turn %= PLAYERS
            turnctr += 1
            movectr += 1
    elif(move==3):
        # if(turn==0 and players[1].hand[1]>0 and turnctr>25):
        #     players[1].hand[1] -= 1;
        #     players[1].numCards -= 1;
        
        # else:
            toDraw -= 1;
            if(toDraw==0): turn += 1; turn %= PLAYERS; toDraw = 1;
            turnctr += 1
            movectr += 1
    elif(move==4):
        # if(turn==0 and players[1].hand[1]>0):
        #     players[1].hand[1] -= 1;
        #     players[1].numCards -= 1;
        # else:
            favorcard = players[victim].getFavored()
            # print('favorcard', favorcard)
            players[turn].hand[favorcard] += 1 
            players[turn].numCards += 1
            players[turn].inform(turn, move, {'victim': victim, 'cardtaken': favorcard})
    elif(move==5):
        rng.shuffle(deck)
    elif(move==6):
        players[turn].inform(turn,6,deck[:-4:-1])
    elif(move>=7):
        # if(turn==0 and players[1].hand[1]>0):
        #     players[1].hand[1] -= 1;
        #     players[1].numCards -= 1;
        # else:
            cardtaken = random.choices([0,1,2,3,4,5,6,7,8,9,10,11], weights=players[victim].hand, k=1)[0]
            players[victim].hand[cardtaken] -= 1
            players[victim].numCards -= 1
            players[victim].inform(turn, move, {'victim': victim, 'cardtaken': cardtaken})
            players[turn].hand[cardtaken] += 1
            players[turn].numCards += 1
            players[turn].inform(turn, move, {'victim': victim, 'cardtaken': cardtaken})
    elif(move==0):
        nextcard = deck.pop()
        print('nextcard', nextcard)
        safe = players[turn].cardDrawn(nextcard)
        print('issafe', safe, type(safe))
        movectr += 1
        if(safe==0): print('notsafereturn'); return (players, turn, turnctr, movectr, victim, toDraw, deck, turn^1)
        else:
            if(safe==1): 
                if(not deck): deck = [-1]
                else:
                    print('from game run toDraw',toDraw,'turn', turn)
                    deck.insert(players[turn].reinsertEK(len(deck)),-1)
            toDraw -= 1
            if(toDraw <= 0): turn += 1; turn %= PLAYERS; toDraw = 1; turnctr += 1
    return (players, turn, turnctr, movectr, victim, toDraw, deck, False)

def processMove(move, players, turn, turnctr, movectr, victim, toDraw, deck):
    return simulateMove(move, players, turn, turnctr, movectr, victim, toDraw, deck)


def initGame(PLAYERS):
    deck = [1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11]
    playerdecks = [[1]+[0]*11 for n in range(PLAYERS)] #0 = me, 1+ = AIs
    players = []
    initDeck(deck, playerdecks, players, PLAYERS)
    turn = 0
    turnctr = 0 # Number of cards drawn from deck
    movectr = 0 # Number of ATK + SKIP + Cards Drawn
    victim = 1
    toDraw = 1
    return (players, turn, turnctr, movectr, victim, toDraw, deck)
