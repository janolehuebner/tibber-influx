# Pull base image
#TODO better base image and structure
FROM ubuntu:22.04

# Labels
LABEL MAINTAINER="Øyvind Nilsen <oyvind.nilsen@gmail.com>"

# Setup external package-sources
RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python3-setuptools \
    python3-pip \
    gcc \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* 

# Run pip install
RUN pip install pytz --upgrade
RUN pip install tzdata --upgrade
ADD requirenments.txt /
RUN pip3 install -r /requirenments.txt
# Environment
ENV PYTHONIOENCODING=utf-8
ADD pulse.py /

# Chmod
RUN chmod 755 /pulse.py

CMD ["/bin/python3","/pulse.py"]