FROM python:3.7-alpine
COPY bots/config.py /bots/
COPY requirements.txt /tmp
COPY bots/twitter_bot.py /bots/
COPY bots/followed.txt /bots/
RUN pip3 install -r /tmp/requirements.txt
WORKDIR /bots
CMD ["python3", "twitter_bot.py"]

