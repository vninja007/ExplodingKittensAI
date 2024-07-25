import random

randomlist = [int(i) for i in open('random256.txt').readlines()]
startind = random.randint(0,len(randomlist)//10)



class Player: #RandomPlayer
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand
    def inform(self, player, move, moveData):
        pass
    def getMove(self, toDraw, movectr, turnctr, deckhandlens):
        #Return None = draw ONE card
        psbls = whatcaniplay(self.hand,self.name,deckhandlens)+[None]
        chosenmove = random.choice(psbls)
        # print(self.name, movectr, turnctr, chosenmove, self.hand)
        return chosenmove
    def cardDrawn(self,card): #THIS CANNOT BE OVERWRITTEN
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
    def reinsertEK(self, decklen):
        return random.randint(0, decklen)

    


class ARPlayer(Player): #AlternateRandomPlayer
    def getMove(self, toDraw, movectr, turnctr, deckhandlens):
    #Return None = draw ONE card
        global startind
        startind += 1; startind %= 100000
        # print(startind)
        psbls = whatcaniplay(self.hand,self.name,deckhandlens)
        if(not psbls):
            return None
        else:
            playcard = randomlist[startind]%2
            if(not playcard):
                return None
            else:
                return psbls[randomlist[startind]%len(psbls)]
        # chosenmove = random.choice(psbls)

class CommonSensePlayer(Player): #CommonSensePlayer
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand
        self.movehistory = {}
    def inform(self, player, move, moveData):
        pass
    def getMove(self, toDraw, movectr, turnctr, deckhandlens):
        #Return None = draw ONE card
        if(movectr not in self.movehistory): self.movehistory[movectr] = set()

        psbls = whatcaniplay(self.hand,self.name,deckhandlens)+[None]
        chosenmove = random.choice(psbls)

        if('STF' in self.movehistory[movectr]):
            while(chosenmove == 'STF'): 
                # print('stf', chosenmove, self.hand)
                chosenmove = random.choice(psbls)
        if('SHUF' in self.movehistory[movectr]):
            while(chosenmove == 'SHUF'): chosenmove = random.choice(psbls)
        # print(self.name, movectr, turnctr, chosenmove, self.hand)
        self.movehistory[movectr].add(chosenmove)
        return chosenmove
    def getFavored(self):
        index = random.randrange(len(self.hand))
        pickable = [i for i in self.hand if i!='DEF' and i!='FVR' and i!='NOPE']
        if(not pickable):
            if('NOPE' in self.hand): 
                self.hand.remove('NOPE')
                return 'NOPE'
            if('FVR' in self.hand): 
                self.hand.remove('FVR')
                return 'FVR'
            self.hand.remove('DEF')
            return 'DEF'
            
            
        chosen = pickable.pop(random.randrange(len(pickable)))
        self.hand.remove(chosen)
        return chosen
        # return self.hand.pop(random.randrange(len(self.hand)))

class RunningPlayer(CommonSensePlayer):
    def getMove(self, toDraw, movectr, turnctr, deckhandlens):
        global startind
        # startind += 1; startind %= 100000
        # playcard = randomlist[startind]%2
        # if(not playcard): return None
        if(turnctr<15): return None
        if(turnctr<35 and self.hand.count('DEF')): return None
        # if(turnctr<20): return None
        handset = set(self.hand)
        if(movectr not in self.movehistory): self.movehistory[movectr] = set()

        psbls = whatcaniplay(self.hand,self.name,deckhandlens)+[None]
        catcards = [i for i in psbls if type(i)==str and i[0]=='C']
        if(catcards): return catcards[0]

        

        chosenmove = random.choice(psbls)

        if('STF' in self.movehistory[movectr]):
            while(chosenmove == 'STF'): 
                # print('stf', chosenmove, self.hand)
                chosenmove = random.choice(psbls)
        if('SHUF' in self.movehistory[movectr]):
            while(chosenmove == 'SHUF'): chosenmove = random.choice(psbls)
        # print(self.name, movectr, turnctr, chosenmove, self.hand)
        self.movehistory[movectr].add(chosenmove)
        return chosenmove
    
    def reinsertEK(self, decklen):
        return 1





    
def whatcaniplay(deck,name,deckhandlens):
    possible = []
    # print(mappign)
    victim = int(name)^1
    if((cnt:=deck.count('ATK'))): possible += ['ATK']*cnt
    if((cnt:=deck.count('SKIP'))): possible += ['SKIP']*cnt
    if((cnt:=deck.count('SHUF'))): possible += ['SHUF']*cnt
    if((cnt:=deck.count('FVR')) and deckhandlens[victim]): possible += ['FVR']*cnt
    if((cnt:=deck.count('STF'))): possible += ['STF']*cnt
    if((cnt:=deck.count('C1')) and deckhandlens[victim]): possible += ['C1']*(cnt//2)
    if((cnt:=deck.count('C2')) and deckhandlens[victim]): possible += ['C2']*(cnt//2)
    if((cnt:=deck.count('C3')) and deckhandlens[victim]): possible += ['C3']*(cnt//2)
    if((cnt:=deck.count('C4')) and deckhandlens[victim]): possible += ['C4']*(cnt//2)
    if((cnt:=deck.count('C5')) and deckhandlens[victim]): possible += ['C5']*(cnt//2)

    
    # mapping = {card:deck.count(card) for card in deck}
    # if('ATK' in mapping): possible += ['ATK']*mapping['ATK']
    # if('SKIP' in mapping): possible += ['SKIP']*mapping['SKIP']
    # if('SHUF' in mapping): possible += ['SHUF']*mapping['SHUF']
    # if('FVR' in mapping and deckhandlens[int(name)^1]): possible += ['FVR']*mapping['FVR']
    # if('STF' in mapping): possible += ['STF']*mapping['STF']
    # if('C1' in mapping and deckhandlens[int(name)^1]): possible += ['C1']*(mapping['C1']//2)
    # if('C2' in mapping and deckhandlens[int(name)^1]): possible += ['C2']*(mapping['C2']//2)
    # if('C3' in mapping and deckhandlens[int(name)^1]): possible += ['C3']*(mapping['C3']//2)
    # if('C4' in mapping and deckhandlens[int(name)^1]): possible += ['C4']*(mapping['C4']//2)
    # if('C5' in mapping and deckhandlens[int(name)^1]): possible += ['C5']*(mapping['C5']//2)
    return possible

def LCG(x, a, c, m): #https://www.ams.org/journals/mcom/1999-68-225/S0025-5718-99-00996-5/S0025-5718-99-00996-5.pdf
    return (a*x+c)%m