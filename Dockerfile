FROM python:3.12-slim-bookworm
WORKDIR /app
LABEL MAINTAINER="Jan-Ole Hübner <huebner@jan-ole.de>"

ADD requirements.txt /app
RUN pip3 install -r /app/requirements.txt

ENV PYTHONIOENCODING=utf-8

ADD . /app

RUN chmod 755 /app/pulse.py /app/get_price.py /app/start.sh

CMD ["/app/start.sh"]
