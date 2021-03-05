FROM python:3.7
COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install -y ffmpeg
RUN wget https://github.com/robinhad/voice-recognition-ua/releases/download/v0.3/uk.tflite
RUN wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.1/deepspeech-0.9.1-models.tflite
RUN pip install -r requirements.txt
CMD uwsgi app.ini --http 0.0.0.0:$PORT
