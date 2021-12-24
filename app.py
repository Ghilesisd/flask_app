from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')

def homepage():
    return "hello vs code"
    return render_template("base.html")

def hello():
        return "hello"
def engister()
        return "enregister"
if __name__ == '__main__':
    app.run(debug=True)
