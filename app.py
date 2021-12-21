from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def homepage():
<<<<<<< HEAD
    return "hi "
=======
    return "new line"
