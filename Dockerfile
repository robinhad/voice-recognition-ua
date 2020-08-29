FROM python:3.7
COPY . /app
WORKDIR /app
RUN wget https://github.com/robinhad/voice-recognition-ua/releases/download/0.1/uk.tflite
RUN pip install -r requirements.txt
CMD ["uwsgi", "app.ini"]