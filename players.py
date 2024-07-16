import random

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

class CommonSensePlayer(Player): #RandomPlayer
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
