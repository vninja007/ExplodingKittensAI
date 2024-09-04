import random
from players import *
import time; ctic = time.time()

#Deck Structure


#[DEF, NOPE, ATK, SKIP, FVR, SHUF, STF, C1, C2, C3, C4, C5]
#[0.   1,    2,   3,    4,   5,    6,   7,  8,  9, 10, 11]

#EXPL = -1

def initDeck(deck, playerdecks, players, PLAYERS):
    # deck.extend([1 for i in range(5)])
    # deck.extend([2 for i in range(4)])
    # deck.extend([3 for i in range(4)])
    # deck.extend([4 for i in range(4)])
    # deck.extend([5 for i in range(4)])
    # deck.extend([6 for i in range(5)])

    # deck.extend([7 for i in range(4)])
    # deck.extend([8 for i in range(4)])
    # deck.extend([9 for i in range(4)])
    # deck.extend([10 for i in range(4)])
    # deck.extend([11 for i in range(4)])

    # deck = [1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11]

    rng.shuffle(deck)
    # deck = selfshuffle(deck)
    # print(playerdecks)
    for player in playerdecks:
        for i in range(7):
            player[deck.pop()]+=1


    deck.extend([0 for i in range(1+(PLAYERS<5))])
    deck.extend([-1 for i in range(PLAYERS-1)])

    rng.shuffle(deck)
    players.append(Player(0,playerdecks[0]))
    players.append(CommonSensePlayer(1,playerdecks[1]))


# while len(players):


def simulateGame(PLAYERS):
    deck = [1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11]
    playerdecks = [[1]+[0]*11 for n in range(PLAYERS)] #0 = me, 1+ = AIs
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
            move = players[turn].getMove(toDraw, movectr, turnctr, [players[0].numCards, players[1].numCards])
            
            if(move):
                players[turn].numCards -= 1
                playerdecks[turn][move] -= 1
                if(move>=7):
                    players[turn].numCards -= 1
                    playerdecks[turn][move] -= 1
            victim = turn^1
            # print('turn', turn, playerdecks[0], playerdecks[1], 'np0', players[0].numPlayable, 'np1', players[1].numPlayable, 'lendeck', len(deck), 'move', move)
            
            if(not move): continue
            # for player in players:
            #     player.inform(turn, move, victim if move==4 or move>=7 else None)

            if(move==2):
                toDraw = toDraw+1 if toDraw==1 else toDraw+2
                turn += 1; turn %= PLAYERS
                turnctr += 1
                movectr += 1
            elif(move==3):
                turn += 1; turn %= PLAYERS
                turnctr += 1
                movectr += 1
            elif(move==4):
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
                cardtaken = random.choices([0,1,2,3,4,5,6,7,8,9,10,11], weights=players[victim].hand, k=1)[0]
                # print('cardtaken', cardtaken)
                players[victim].hand[cardtaken] -= 1
                players[victim].numCards -= 1
                players[victim].inform(turn, move, {'victim': victim, 'cardtaken': cardtaken})
                players[turn].hand[cardtaken] += 1
                players[turn].numCards += 1
                players[turn].inform(turn, move, {'victim': victim, 'cardtaken': cardtaken})
        # print(deck)
        nextcard = deck.pop()
        # print('nextcard', nextcard)
        safe = players[turn].cardDrawn(nextcard)
        movectr += 1
        if(not safe): players.pop(turn); toDraw = 1
        else:
            if(safe==1): 
                if(not deck): deck = [-1]
                else:
                    deck.insert(players[turn].reinsertEK(len(deck)),-1)
            toDraw -= 1
            if(toDraw == 0): turn += 1; turn %= PLAYERS; toDraw = 1; turnctr += 1
    return players[0].name

# print(players[0].hand)
# print("Player",players[0].name,"won by",players[0].hand.count('DEF'),'defuses')
# print(players[0].getMove())

if __name__ == '__main__':
    onewin = 0
    zerowin = 0
    for _ in range(int(1e4)):
        res = simulateGame(2)
        # print(res)
        if(res==1): onewin += 1
        else: zerowin += 1

    print(zerowin, onewin, zerowin/(onewin+zerowin), onewin/(onewin+zerowin))
    print(time.time()-ctic)