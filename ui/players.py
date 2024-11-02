import random
import numpy as np
rng = np.random.default_rng()

randomlist = [int(i) for i in open('random256.txt').readlines()]
startind = random.randint(0,len(randomlist)//10)

class Player: #RandomPlayer
    def __init__(self, name, hand):
        self.name = name
        self.numPlayable = sum(hand[2:7]) + sum([hand[i]//2 for i in range(7,12)])
        self.numCards = 8
        self.hand = hand
    
    def inform(self, player, move, moveData):
        if(player!=self.name and move>=7 and moveData['victim']==int(self.name)):
            cardtaken = moveData['cardtaken']
            if(2<=cardtaken<=6): self.numPlayable -= 1
            elif(cardtaken >= 7 and self.hand[cardtaken]%2==1): self.numPlayable -= 1
            return
        if(player==self.name and (move==4 or move>=7)):
            cardtaken = moveData['cardtaken']
            if(2<=cardtaken<=6): self.numPlayable += 1
            elif(cardtaken >= 7 and self.hand[cardtaken]%2==0): self.numPlayable += 1

        
    def getMove(self, toDraw, movectr, turnctr, deckhandlens):
        #Return None = draw ONE card
        chosenmove = giveRandomMove(self.hand,self.name,deckhandlens, self.numPlayable)
        if(chosenmove!=None): self.numPlayable -= 1
        # print('moving!', self.name, chosenmove)
        return chosenmove
    def cardDrawn(self,card): #THIS CANNOT BE OVERWRITTEN
        if(card==-1):
            if(not self.hand[0]):
                return 0
            else:
                self.hand[0] -= 1
                self.numCards -= 1
                return 1
        else:
            self.hand[card] += 1
            self.numCards += 1
            if(card >= 7): #catcard
                if(self.hand[card]%2==0):
                    self.numPlayable += 1
            elif(card >= 2): #not catcard, but still playable
                self.numPlayable += 1
            return 2
    def getFavored(self):
        togiveaway = random.choices([0,1,2,3,4,5,6,7,8,9,10,11], weights=self.hand, k=1)[0]
        self.hand[togiveaway] -= 1
        self.numCards -= 1
        if(2 <= togiveaway <= 6): self.numPlayable -= 1
        elif(togiveaway >= 7 and self.hand[togiveaway]%2==1): self.numPlayable -= 1
        return togiveaway
    def reinsertEK(self, decklen):
        return int(random.random()*(decklen+1))


class CommonSensePlayer(Player): #CommonSensePlayer
    def __init__(self, name, hand):
        super().__init__(name,hand)
        self.movehistory = {}

    def getMove(self, toDraw, movectr, turnctr, deckhandlens):
        #Return None = draw ONE card
        if(movectr not in self.movehistory): self.movehistory[movectr] = set()
        presets = {}
        
        if(6 in self.movehistory[movectr]): presets[6] = 0
        if(5 in self.movehistory[movectr]): presets[5] = 0

        chosenmove = giveRandomMove(self.hand,self.name,deckhandlens, self.numPlayable,victim=None,includeNone=True,presets=presets)

        
        self.movehistory[movectr].add(chosenmove)
        return chosenmove
    def getFavored(self):
        favortables = list(self.hand)
        x = sum(self.hand)
        if(self.hand[0]!=x):
            x -= self.hand[0]
            favortables[0] = 0
            if(self.hand[4]!=x):
                x -= self.hand[4]
                favortables[4] = 0
                if(self.hand[1]!=x):
                    x -= self.hand[1]
                    favortables[1] = 0
        togiveaway = random.choices([0,1,2,3,4,5,6,7,8,9,10,11], weights=favortables, k=1)[0]
        self.hand[togiveaway] -= 1
        self.numCards -= 1
        if(2 <= togiveaway <= 6): self.numPlayable -= 1
        elif(togiveaway >= 7 and self.hand[togiveaway]%2==1): self.numPlayable -= 1
        return togiveaway
            
            

class RunningPlayer(CommonSensePlayer):
    def getMove(self, toDraw, movectr, turnctr, deckhandlens):
        global startind
        if(turnctr<35 and self.hand[0]): return None
        handset = set(self.hand)
        if(movectr not in self.movehistory): self.movehistory[movectr] = set()
        presets = {6:0}
        
        if(6 in self.movehistory[movectr]): presets[6] = 0
        if(5 in self.movehistory[movectr]): presets[5] = 0
        psbls = givePsbls(self.hand,self.name,deckhandlens,None,presets)
        if(psbls[4]): self.numPlayable -= 1; return 4;
        if(psbls[7]): self.numPlayable -= 1; return 7;
        if(psbls[8]): self.numPlayable -= 1; return 8;
        if(psbls[9]): self.numPlayable -= 1; return 9;
        if(psbls[10]): self.numPlayable -= 1; return 10;
        if(psbls[11]): self.numPlayable -= 1; return 11;
    

        
        if(toDraw > 1 and psbls[2]): self.numPlayable -= 1; return 2;
        if(toDraw>1 and psbls[3]): self.numPlayable -= 1; return 3
        if(movectr>40 and psbls[2]): self.numPlayable -= 1; return 2
        if(movectr>40 and psbls[3]): self.numPlayable -= 1; return 3


        if(psbls==[0]*12): return None
        chosenmove = random.choices([0,1,2,3,4,5,6,7,8,9,10,11], weights=psbls, k=1)[0]
        if (chosenmove): self.numPlayable -= 1;
        self.movehistory[movectr].add(chosenmove)
        return chosenmove
    
    def reinsertEK(self, decklen):
        return 3


def weighted_random_choice(choices, weights):
    cum_weights = np.cumsum(weights)
    total_weight = cum_weights[-1]
    rand_val = np.random.rand() * total_weight
    idx = np.searchsorted(cum_weights, rand_val)
    return choices[idx]

def givePsbls(deck,name,deckhandlens,victim=None,presets={}):
    if(victim == None): victim = 1 if int(name)==0 else 0

    possible = list(deck)
    possible[0] = 0
    possible[1] = 0
    if deckhandlens[victim]:
        possible[7] = possible[7]//2
        possible[8] = possible[8]//2
        possible[9] = possible[9]//2
        possible[10] = possible[10]//2
        possible[11] = possible[11]//2
    else:
        possible[4] = 0
        possible[7] = 0
        possible[8] = 0
        possible[9] = 0
        possible[10] = 0
        possible[11] = 0

    for i in presets:
        possible[i] = presets[i]
    return possible

    
def giveRandomMove(deck,name,deckhandlens,numPlayable,victim=None,includeNone=True,presets={}):
    
    if(numPlayable == 0): return None
    if(includeNone and not int(random.random()*(numPlayable+1))): return None
    
    possible = givePsbls(deck, name, deckhandlens, victim, presets)
    
    if(possible==[0]*12): return None
    numbers = [0,1,2,3,4,5,6,7,8,9,10,11]
    return random.choices(numbers, weights=possible, k=1)[0]
