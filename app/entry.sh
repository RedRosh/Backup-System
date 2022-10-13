#!/bin/bash
# Generating the user documentation
pdoc --html . && cp -r html/app doc/ && rm -rf html
chmod -R 777 doc
# Starting the Cron in foreground to avoid quiting the container
cron -f