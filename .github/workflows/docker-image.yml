FROM python:3.8-slim-buster

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git

COPY requirements.txt /requirements.txt

RUN pip3 install --no-cache-dir -r /requirements.txt

WORKDIR /cd
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/bin/bash", "/start.sh"]
