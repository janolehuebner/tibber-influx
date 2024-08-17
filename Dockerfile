FROM python:3.12-slim-bookworm
WORKDIR /app
LABEL MAINTAINER="Jan-Ole Hübner <huebner@jan-ole.de>"

RUN apt-get update && apt-get install -y cron

ADD requirements.txt /app
RUN pip3 install -r /requirements.txt

ENV PYTHONIOENCODING=utf-8

ADD . /app


RUN echo "*/2 * * * * /app/delay_price.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/get_price

RUN chmod 0644 /etc/cron.d/get_price

RUN crontab /etc/cron.d/get_price

RUN touch /var/log/cron.log

RUN chmod 755 /app/pulse.py /app/get_price.py /app/start.sh /app/delay_price.sh

CMD ["/app/start.sh"]
