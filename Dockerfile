FROM python:3.12

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y ffmpeg \
 && pip install --no-cache-dir -r requirements.txt

EXPOSE 5002

ENV FLASK_ENV=production

CMD ["flask", "run", "--host=0.0.0.0", "--port=5002"]