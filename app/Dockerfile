FROM python
RUN apt-get update && apt-get -y install cron vim dos2unix wait-for-it
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
COPY ./jobs/crontab /etc/cron.d/crontab
RUN find /etc/cron.d/ -type f -print0 | xargs -0 dos2unix
RUN find entry.sh -type f -print0 | xargs -0 dos2unix
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
RUN touch ./logs/logs.log
RUN chmod 777 ./logs/logs.log
RUN chmod +x entry.sh

