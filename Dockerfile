FROM python:3.10-slim

# Labels
LABEL MAINTAINER="Jan-Ole Hübner <huebner@jan-ole.de>"


ADD requirenments.txt /
RUN pip3 install -r /requirenments.txt
# Environment
ENV PYTHONIOENCODING=utf-8
ADD . /

# Chmod
RUN chmod 755 /pulse.py
CMD ["python3","/get_price.py"]
CMD ["python3","/pulse.py"]