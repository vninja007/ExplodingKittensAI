from flask import Flask, render_template, request, jsonify
from flask_assets import Bundle, Environment
from maingamerun import *
from players import *
import random
app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/style.css", output="dist/main.css")

assets.register("css", css)
css.build()

decklen = 35
isOver = False

players, turn, turnctr, movectr, victim, toDraw, deck = initGame(2)
playerhand = players[0].hand
print(playerhand)
print(deck)

@app.route("/")
def homepage():
    return render_template("index.html", legalmoves = playerhand, decklen = decklen, enumerate=enumerate)

@app.route('/image_clicked/<int:image_id>')
def image_clicked(image_id):
    global decklen, playerhand, players, turn, turnctr, movectr, victim, toDraw, deck, isOver
    if(type(isOver)==bool):
        # print(image_id, turn)
        print('deck before human', deck)
        if(2 <= image_id <= 6 and playerhand[image_id] >= 1):
            # playerhand[image_id] -= 1
            players, turn, turnctr, movectr, victim, toDraw, deck, isOver = processMove(image_id, players, turn, turnctr, movectr, victim, toDraw, deck)
        elif(7 <= image_id <= 11 and playerhand[image_id] >= 2):
            # playerhand[image_id] -= 2
            players, turn, turnctr, movectr, victim, toDraw, deck, isOver = processMove(image_id, players, turn, turnctr, movectr, victim, toDraw, deck)
        # print
        elif(image_id==100):
            # decklen -= 1
            players, turn, turnctr, movectr, victim, toDraw, deck, isOver = processMove(0, players, turn, turnctr, movectr, victim, toDraw, deck)
        playerhand = players[0].hand
        
        print('humanplay', image_id, 'isnowturn', turn, 'toDraw', toDraw, 'deck after', deck)
        if(image_id in {2, 3, 100, 0}):
            print('turnis', turn, 'isover', isOver)
            while(turn == 1 and type(isOver)==bool): #definite winner
                aimove = players[turn].getMove(toDraw, movectr, turnctr, [players[0].numCards, players[1].numCards]) or 0
                print('aiplay', aimove, 'deck before', deck)
                players, turn, turnctr, movectr, victim, toDraw, deck, isOver = processMove(aimove, players, turn, turnctr, movectr, victim, toDraw, deck)
                
                print('isover after ai', isOver)
        # print(isOver)

    return jsonify({f'card{i}':playerhand[i] for i in range(12)} | {'decklen': len(deck)} | {'turn': turn} | {'isOver': isOver} |{'toDraw': toDraw})
    
    
    

if __name__ == "__main__":
    app.run(debug=True)