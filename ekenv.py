

import random
import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding
rng = np.random.default_rng()

def initDeck(PLAYERS):
    deck = [1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11]
    rng.shuffle(deck)
    if(PLAYERS==2):
        me = [0]*12
        me[0] = 1
        for i in range(7):
            me[deck.pop()]+=1
        op = [0]*12
        op[0] = 1
        for i in range(7):
            op[deck.pop()]+=1
        deck.extend([0 for i in range(1+(PLAYERS<5))])
        deck.extend([-1 for i in range(PLAYERS-1)])
        rng.shuffle(deck)
        return deck, me, op
    else:
        raise NotImplementedError
    
def giveRandomMove(deck,name,deckhandlens,numPlayable,victim=None,includeNone=True):
    
    if(numPlayable == 0): return None
    # print(numPlayable, deck, deckhandlens)
    if(includeNone and not int(random.random()*(numPlayable+1))): return None
    # if(includeNone and not random.randint(0,numPlayable)): return None
    
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

    if(possible==[0]*12): return None
    numbers = [0,1,2,3,4,5,6,7,8,9,10,11]

    # return weighted_random_choice(numbers, possible)
    return random.choices(numbers, weights=possible, k=1)[0]

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

        
    def getMove(self, deckhandlens):
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


class ExplodingKittensEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self): #changed
        super(ExplodingKittensEnv, self).__init__()
        
        # Initialize the blackjack deck.

        self.deck, self.hand1, self.hand2 = initDeck(2)
        self.me = 0
        self.op = 1
        self.lastcard3 = 0
        self.lastcard2 = 0
        self.lastcard = 0
        self.toDraw = 1
        self.movectr = 0
        self.turnctr = 0
        self.isfirstmove = True
        self.players = [Player(0,self.hand1),Player(1,self.hand2)]
        
        # self.reward_options = {"lose":-100, "tie":0, "win":100}
        

        #Number of possible outputs
        self.action_space = spaces.Discrete(11) #n-1, 0 = Take Card
        
        
        #Number of possible inputs
        self.observation_space = spaces.Tuple((
            spaces.Discrete(6), #DEFUSE 
            spaces.Discrete(5), #NOPE
            spaces.Discrete(4), #ATTACK
            spaces.Discrete(4), #SKIP
            spaces.Discrete(4), #FAVOR
            spaces.Discrete(4), #SHUFFLE
            spaces.Discrete(5), #STF
            spaces.Discrete(4), #C1
            spaces.Discrete(4), #C2
            spaces.Discrete(4), #C3
            spaces.Discrete(4), #C4
            spaces.Discrete(4), #C4
            spaces.Discrete(4), #C5
            spaces.Discrete(57), #Num Left In deck
            spaces.Discrete(8), #Num cards you have to take
            spaces.Discrete(12), #Last Card
            spaces.Discrete(12), #2nd Last Move
            spaces.Discrete(12), #3rd Last Move
            spaces.Discrete(57), #Num cards opponent has
            spaces.Discrete(57), #Num moves played
            ))
        
        self.done = False

    def _process_move(self, turn, move):
        # move = self.players[turn].getMove(self.toDraw, self.movectr, self.turnctr, [self.players[0].numCards, self.players[1].numCards])
        turn %= 2
        if(move):
            self.lastcard3 = self.lastcard2
            self.lastcard2 = self.lastcard
            self.lastcard = move
            self.players[turn].numCards -= 1
            self.players[turn].hand[move] -= 1
            if(move>=7):
                self.players[turn].numCards -= 1
                self.players[turn].hand[move] -= 1
        victim = turn^1
        # print('turn', turn, playerdecks[0], playerdecks[1], 'np0', players[0].numPlayable, 'np1', players[1].numPlayable, 'lendeck', len(deck), 'move', move)
        
        # for player in players:
        #     player.inform(turn, move, victim if move==4 or move>=7 else None)

        if(move==2):
            self.toDraw = self.toDraw+1 if self.toDraw==1 else self.toDraw+2
            turn += 1; turn %= 2
            self.turnctr += 1
            self.movectr += 1
        elif(move==3):
            turn += 1; turn %= 2
            self.turnctr += 1
            self.movectr += 1
        elif(move==4):
            favorcard = self.players[victim].getFavored()
            # print('favorcard', favorcard)
            self.players[turn].hand[favorcard] += 1 
            self.players[turn].numCards += 1
            self.players[turn].inform(turn, move, {'victim': victim, 'cardtaken': favorcard})
        elif(move==5):
            rng.shuffle(self.deck)
        elif(move==6):
            self.players[turn].inform(turn,6,self.deck[:-4:-1])
        elif(move>=7):
            cardtaken = random.choices([0,1,2,3,4,5,6,7,8,9,10,11], weights=self.players[victim].hand, k=1)[0]
            # print('cardtaken', cardtaken)
            self.players[victim].hand[cardtaken] -= 1
            self.players[victim].numCards -= 1
            self.players[victim].inform(turn, move, {'victim': victim, 'cardtaken': cardtaken})
            self.players[turn].hand[cardtaken] += 1
            self.players[turn].numCards += 1
            self.players[turn].inform(turn, move, {'victim': victim, 'cardtaken': cardtaken})
        # print(self.deck)
        if not move:
            nextcard = self.deck.pop()
            # print('nextcard', nextcard)
            safe = self.players[turn].cardDrawn(nextcard)
            self.movectr += 1
            if(not safe): return turn^1; #players.pop(turn); self.toDraw = 1
            else:
                if(safe==1): 
                    if(not self.deck): self.deck = [-1]
                    else:
                        self.deck.insert(self.players[turn].reinsertEK(len(self.deck)),-1)
                self.toDraw -= 1
                if(self.toDraw == 0): turn += 1; turn %= 2; self.toDraw = 1; self.turnctr += 1
        return -1
    
    def doEvaluation(self,winner):
        result = 0
        result = result+100 if winner==self.me else result-100
        result += 5*(self.players[self.me].hand[0] - self.players[self.op].hand[0])
        result += 2*(self.players[self.me].hand[2] - self.players[self.op].hand[2])
        result += (self.players[self.me].hand[3] - self.players[self.op].hand[3])
        return result

    def _take_action(self, move):
        if(self.isfirstmove and self.me == 1):
            self.isfirstmove = False
            
            opmove = self.players[0].getMove([self.players[0].numCards, self.players[1].numCards])
            res = self._process_move(0,opmove)
            if(res!=-1): return (res, self.doEvaluation(res))
        
        res = self._process_move(self.me, move)
        if(res!=-1): return (res, self.doEvaluation(res))
        
        opmove = self.players[0].getMove([self.players[0].numCards, self.players[1].numCards])
        res = self._process_move(self.op,opmove)
        if(res!=-1): return (res, self.doEvaluation(res))


        return -1
 



    def step(self, action):
        status = self._take_action(action)
        
        # End the episode/game is the player stands or has a hand value >= 21.
        self.done = type(status) == tuple
        
        # rewards are 0 when the player hits and is still below 21, and they
        # keep playing.
        rewards = 0 if type(status) != tuple else status[1]
        
        # the state is represented as a player hand-value + dealer upcard pair.
        obs = self.players[self.me].hand + [len(self.deck)] + [self.toDraw,self.lastcard,self.lastcard2,self.lastcard3] + [len(self.players[self.op].hand)] + [self.movectr]
        # obs = np.array([player_value_obs, upcard_value_obs])
        
        return obs, rewards, self.done, {}
    
    def reset(self): # Changed


        self.deck, self.hand1, self.hand2 = initDeck(2)
        self.me = 0
        self.op = 1
        self.lastcard3 = 0
        self.lastcard2 = 0
        self.lastcard = 0
        self.toDraw = 1
        self.movectr = 0
        self.turnctr = 0
        self.isfirstmove = True
        self.players = [Player(0,self.hand1),Player(1,self.hand2)]
        
        # the state is represented as a player hand-value + dealer upcard pair.
        obs = self.players[self.me].hand + [len(self.deck)] + [1,0,0,0] + [len(self.players[self.op].hand)] + [0]
        return np.array(obs)
    
    def render(self, mode='human', close=False): #Changed
        # convert the player hand into a format that is
        # easy to read and understand.
        print(f'Hand: {self.players[self.me].hand} | Cards: {self.players[self.me].numCards} | Effectives: {self.players[self.me].hand[2] * 2 + self.players[self.me].hand[3]}')
        print()
