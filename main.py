from flask import Flask, render_template, request
from io import BytesIO
from client import client
import telebot
import logging
import os
import warnings
from client import client
from io import BytesIO
import pydub

warnings.simplefilter('ignore')
TOKEN = os.environ['TOKEN']

if not TOKEN:
    print('You must set the TOKEN environment variable')
    exit(1)

START_MSG = '''Вітання!
Цей бот створений для тестування перекладу українських аудіозаписів в текст.
Група для обговорення: https://t.me/speech_recognition_uk'''

FIRST_STEP = '''Використовувати бота просто: надішліть аудіоповідомлення і чекайте відповіді'''


bot = telebot.TeleBot(TOKEN, parse_mode=None)
app = Flask(__name__,)
app.config['MAX_CONTENT_LENGTH'] = 120 * 1024


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


@app.route('/bot/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/bot")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(
        url='https://voice-recognition-ua.herokuapp.com/bot/' + TOKEN)
    return "!", 200


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, START_MSG)
    bot.reply_to(message, FIRST_STEP)


@bot.message_handler(content_types=['voice'])
def process_voice_message(message):
    # download the recording
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    # create in-memory representation of files
    source_audio = BytesIO()
    source_audio.write(downloaded_file)
    source_audio.seek(0)
    output_audio = BytesIO()
    ogg_file = pydub.AudioSegment.from_ogg(
        source_audio)

    # convert ogg to wav
    ogg_file.set_frame_rate(16000).set_channels(
        1).export(output_audio, "wav", codec="pcm_s16le")
    output_audio.seek(0)

    # do the recognition
    # get the recognized text
    text = client(source_audio)
    # no results
    if not text:
        bot.reply_to(message, 'Я не зміг розпізнати 😢')
    else:
        # send the recognized text
        bot.reply_to(message, text)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
