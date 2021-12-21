from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def homepage():
<<<<<<< HEAD
    return "hello github "
=======
    return "new line"


    return "new test to see if it's working"
