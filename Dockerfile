FROM python:3.12-bookworm

# Labels
LABEL MAINTAINER="Jan-Ole Hübner <huebner@jan-ole.de>"

RUN apt install ca-certificates
ADD requirements.txt /
RUN pip3 install -r /requirements.txt

# Environment
ENV PYTHONIOENCODING=utf-8
ADD . /

# Chmod
RUN chmod 755 /pulse.py
CMD ["python3","/pulse.py"]