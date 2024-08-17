FROM python:3.12-bookworm

# Labels
LABEL MAINTAINER="Jan-Ole Hübner <huebner@jan-ole.de>"

RUN apt-get update && apt-get install -y cron

ADD requirements.txt /
RUN pip3 install -r /requirements.txt

ENV PYTHONIOENCODING=utf-8

ADD . /

RUN echo "*/15 * * * * python3 /get_price.py >> /var/log/cron.log 2>&1" > /etc/cron.d/get_price

RUN chmod 0644 /etc/cron.d/get_price

RUN crontab /etc/cron.d/get_price

RUN touch /var/log/cron.log

RUN chmod 755 /pulse.py

CMD service cron start && python3 /pulse.py