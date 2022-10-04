#!/bin/bash

pdoc --html . && cp -r html/app doc/ && rm -rf html
chmod -R 777 doc
cron -f