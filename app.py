from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def homepage():
<<<<<<< HEAD
    return "hi "
=======
    return "new line"
>>>>>>> 74ceb66ed163901afcdb835d5a357bbc9a91be31
