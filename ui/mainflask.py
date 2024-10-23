from flask import Flask, render_template, request, jsonify
from flask_assets import Bundle, Environment
import random
app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/style.css", output="dist/main.css")

assets.register("css", css)
css.build()


@app.route("/")
def homepage():
    return render_template("index.html", legalmoves =[*range(12)])

@app.route('/image_clicked/<int:image_id>')
def image_clicked(image_id):
    # Process the image click (e.g., log it, update a database, etc.)
    print(image_id)
    return f'Image {image_id} was clicked!'

if __name__ == "__main__":
    app.run(debug=True)