FROM python:slim

WORKDIR /usr/src/voicehelper

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/usr/src:${PYTHONPATH}"

RUN apt-get update && apt-get install libssl-dev -y python3-dev gcc -y musl-dev wget
RUN pip3 install --upgrade pip
COPY . .
RUN pip3 install -r requirements.txt

ENTRYPOINT ["sh", "entrypoint.sh"]
