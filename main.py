from flask import Flask, render_template, request
from io import BytesIO
from client import client

app = Flask(__name__,)


@app.route('/')
def index():
    return render_template('hello.html')


@app.route('/recognize', methods=["POST"])
def recognize():
    file = request.files['file']
    lang = request.form["lang"]
    audio = BytesIO()
    file.save(audio)
    audio.seek(0)
    result = client(audio, lang)
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0')
