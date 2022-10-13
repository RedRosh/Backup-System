FROM python
# Updating the image && installing the dependencies
RUN apt-get update && apt-get -y install cron vim dos2unix wait-for-it
WORKDIR /app
COPY . .
# installing the python dependencies
RUN pip3 install -r requirements.txt
# Setting cron job
COPY ./jobs/crontab /etc/cron.d/crontab
# Setting the permissions && fixing conflict between CL AND CRLF
RUN find /etc/cron.d/ -type f -print0 | xargs -0 dos2unix
RUN find entry.sh -type f -print0 | xargs -0 dos2unix
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
# Creating the log file
RUN touch ./logs/logs.log
# Setting the permissions
RUN chmod 777 ./logs/logs.log
RUN chmod +x entry.sh

