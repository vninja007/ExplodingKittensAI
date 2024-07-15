import random

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
