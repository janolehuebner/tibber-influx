FROM python:3.12-bookworm

# Labels
LABEL MAINTAINER="Jan-Ole Hübner <huebner@jan-ole.de>"

# Install cron
RUN apt-get update && apt-get install -y cron

# Add the requirements
ADD requirements.txt /
RUN pip3 install -r /requirements.txt

# Environment
ENV PYTHONIOENCODING=utf-8

# Add the application code
ADD . /

# Add the cron job
RUN echo "*/15 * * * * python3 /get_price.py >> /var/log/cron.log 2>&1" > /etc/cron.d/get_price

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/get_price

# Apply the cron job
RUN crontab /etc/cron.d/get_price

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Chmod for your main application script
RUN chmod 755 /pulse.py

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
