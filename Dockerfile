# make sure to download https://github.com/robinhad/voice-recognition-ua/releases/download/0.1/uk.tflite
# before build
FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uwsgi", "app.ini"]