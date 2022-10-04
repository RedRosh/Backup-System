FROM python:3.7
RUN apt-get update && apt-get -y install cron vim dos2unix
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY crontab /etc/cron.d/crontab
RUN find /etc/cron.d/ -type f -print0 | xargs -0 dos2unix
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

