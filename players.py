import random

# randomlist = [int(i) for i in open('random256.txt').readlines()]
# startind = random.randint(0,len(randomlist)//10)



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
    def reinsertEK(self, deckstart, decklen):
        return random.randint(deckstart, decklen)

    


# class ARPlayer(Player): #AlternateRandomPlayeri
#     def getMove(self, toDraw, movectr, turnctr, deckhandlens):
#     #Return None = draw ONE card
#         global startind
#         startind += 1; startind %= 100000
#         # print(startind)
#         psbls = whatcaniplay(self.hand,self.name,deckhandlens)
#         if(not psbls):
#             return None
#         else:
#             playcard = randomlist[startind]%2
#             if(not playcard):
#                 return None
#             else:
#                 return psbls[randomlist[startind]%len(psbls)]
#         # chosenmove = random.choice(psbls)

# class CommonSensePlayer(Player): #CommonSensePlayer
#     def __init__(self, name, hand):
#         self.name = name
#         self.hand = hand
#         self.movehistory = {}
#     def inform(self, player, move, moveData):
#         pass
#     def getMove(self, toDraw, movectr, turnctr, deckhandlens):
#         #Return None = draw ONE card
#         if(movectr not in self.movehistory): self.movehistory[movectr] = set()

#         psbls = whatcaniplay(self.hand,self.name,deckhandlens)+[None]
#         chosenmove = random.choice(psbls)

#         if('STF' in self.movehistory[movectr]):
#             while(chosenmove == 'STF'): 
#                 # print('stf', chosenmove, self.hand)
#                 chosenmove = random.choice(psbls)
#         if('SHUF' in self.movehistory[movectr]):
#             while(chosenmove == 'SHUF'): chosenmove = random.choice(psbls)
#         # print(self.name, movectr, turnctr, chosenmove, self.hand)
#         self.movehistory[movectr].add(chosenmove)
#         return chosenmove
#     def getFavored(self):
#         index = random.randrange(len(self.hand))
#         pickable = [i for i in self.hand if i!='DEF' and i!='FVR' and i!='NOPE']
#         if(not pickable):
#             if('NOPE' in self.hand): 
#                 self.hand.remove('NOPE')
#                 return 'NOPE'
#             if('FVR' in self.hand): 
#                 self.hand.remove('FVR')
#                 return 'FVR'
#             self.hand.remove('DEF')
#             return 'DEF'
            
            
#         chosen = pickable.pop(random.randrange(len(pickable)))
#         self.hand.remove(chosen)
#         return chosen
#         # return self.hand.pop(random.randrange(len(self.hand)))

# class RunningPlayer(CommonSensePlayer):
#     def getMove(self, toDraw, movectr, turnctr, deckhandlens):
#         global startind
#         # startind += 1; startind %= 100000
#         # playcard = randomlist[startind]%2
#         # if(not playcard): return None
#         # if(turnctr<15): return None
#         if(turnctr<35 and self.hand.count('DEF')): return None
#         # if(turnctr<20): return None
#         handset = set(self.hand)
#         if(movectr not in self.movehistory): self.movehistory[movectr] = set()

#         psbls = whatcaniplay(self.hand,self.name,deckhandlens)+[None]
#         if('FVR' in psbls): return 'FVR'
#         if('C1' in psbls): return 'C1'
#         if('C2' in psbls): return 'C2'
#         if('C3' in psbls): return 'C3'
#         if('C4' in psbls): return 'C4'
#         if('C5' in psbls): return 'C5'

#         if(toDraw > 1 and 'ATK' in psbls): return 'ATK'
#         if(toDraw>1 and 'SKIP' in psbls): return 'SKIP'
#         if(movectr>40 and 'ATK' in psbls): return 'ATK'
#         if(movectr>40 and 'SKIP' in psbls): return 'SKIP'
#         # catcards = [i for i in psbls if type(i)==str and i[0]=='C']
#         # if(catcards): return catcards[0]



#         chosenmove = random.choice(psbls)

#         if('STF' in self.movehistory[movectr]):
#             while(chosenmove == 'STF'): 
#                 # print('stf', chosenmove, self.hand)
#                 chosenmove = random.choice(psbls)
#         if('SHUF' in self.movehistory[movectr]):
#             while(chosenmove == 'SHUF'): chosenmove = random.choice(psbls)
#         # print(self.name, movectr, turnctr, chosenmove, self.hand)
#         self.movehistory[movectr].add(chosenmove)
#         return chosenmove
    
#     def reinsertEK(self, decklen):
#         return 1





    
def giveRandomMove(deck,name,deckhandlens,numPlayable,victim=None,includeNone=True):
    
    if(numPlayable == 0): return None
    # print(numPlayable, deck, deckhandlens)
    if(includeNone and not random.randint(0,numPlayable)): return None
    if(victim == None): victim = int(name)^1

    possible = list(deck)
    possible[0] = 0
    possible[1] = 0
    possible[4] = possible[4] if deckhandlens[victim] else 0
    possible[7] = possible[7]//2 if deckhandlens[victim] else 0
    possible[8] = possible[8]//2 if deckhandlens[victim] else 0
    possible[9] = possible[9]//2 if deckhandlens[victim] else 0
    possible[10] = possible[10]//2 if deckhandlens[victim] else 0
    possible[11] = possible[11]//2 if deckhandlens[victim] else 0

    if(possible==[0]*12): return None
    numbers = [0,1,2,3,4,5,6,7,8,9,10,11]

    return random.choices(numbers, weights=possible, k=1)[0]

def LCG(x, a, c, m): #https://www.ams.org/journals/mcom/1999-68-225/S0025-5718-99-00996-5/S0025-5718-99-00996-5.pdf
    return (a*x+c)%m