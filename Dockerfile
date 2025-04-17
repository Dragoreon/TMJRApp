FROM python:3.12-slim

WORKDIR /app

COPY . /app
COPY . /bot

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 80

CMD ["sh scripts/deploy-api.sh & sh scripts/deploy-bot.sh"]