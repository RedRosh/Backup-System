#!/bin/bash

pdoc --html . && cp -r html/app doc/ && rm -rf html
cron -f