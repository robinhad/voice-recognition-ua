FROM python:3.7
COPY ./webapp /app
WORKDIR /app
RUN apt-get update
RUN apt-get install -y ffmpeg
RUN wget https://github.com/robinhad/voice-recognition-ua/releases/download/v0.4/uk.tflite
# RUN wget https://github.com/robinhad/voice-recognition-ua/releases/download/v0.4/kenlm.scorer
RUN pip install -r requirements.txt
CMD uwsgi app.ini --http 0.0.0.0:$PORT
