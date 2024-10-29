from flask import Flask, render_template, request, jsonify
from flask_assets import Bundle, Environment
import random
app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/style.css", output="dist/main.css")

assets.register("css", css)
css.build()


playerhand = [*range(12)]
decklen = 35

@app.route("/")
def homepage():
    return render_template("index.html", legalmoves = playerhand, decklen = decklen, enumerate=enumerate)

@app.route('/image_clicked/<int:image_id>')
def image_clicked(image_id):
    global decklen
    print(image_id)

    if(2 <= image_id <= 6 and playerhand[image_id] >= 1):
        playerhand[image_id] -= 1
    if(7 <= image_id <= 11 and playerhand[image_id] >= 2):
        playerhand[image_id] -= 2
    
    if(image_id==100):
        decklen -= 1
    print({f'card{i}':playerhand[i] for i in range(12)})

    return jsonify({f'card{i}':playerhand[i] for i in range(12)} | {'decklen': decklen})
    
    
    
    # return f'Image {image_id} was clicked!'

if __name__ == "__main__":
    app.run(debug=True)