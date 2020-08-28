from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('hello.html')


@app.route('/recognize', methods=["POST"])
def recognize():
    return 'Hello, World!'
