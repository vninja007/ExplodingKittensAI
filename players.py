import random

class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand
    def inform(self, player, move, moveData):
        pass
    def getMove(self, toDraw,deckhandlens):
        #Return None = draw ONE card
        psbls = whatcaniplay(self.hand,self.name,deckhandlens)+[None]
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

    
def whatcaniplay(deck,name,deckhandlens):
    possible = []
    playerdeck = [str(card) for card in deck]
    mapping = {card:playerdeck.count(card) for card in set(playerdeck)}
    # print(mappign)
    if('ATK' in mapping): possible += ['ATK']*mapping['ATK']
    if('SKIP' in mapping): possible += ['SKIP']*mapping['SKIP']
    if('SHUF' in mapping): possible += ['SHUF']*mapping['SHUF']
    if('FVR' in mapping and deckhandlens[int(name)^1]): possible += ['FVR']*mapping['FVR']
    if('STF' in mapping): possible += ['STF']*mapping['STF']
    if('C1' in mapping and deckhandlens[int(name)^1]): possible += ['C1']*(mapping['C1']//2)
    if('C2' in mapping and deckhandlens[int(name)^1]): possible += ['C2']*(mapping['C2']//2)
    if('C3' in mapping and deckhandlens[int(name)^1]): possible += ['C3']*(mapping['C3']//2)
    if('C4' in mapping and deckhandlens[int(name)^1]): possible += ['C4']*(mapping['C4']//2)
    if('C5' in mapping and deckhandlens[int(name)^1]): possible += ['C5']*(mapping['C5']//2)
    return possible
