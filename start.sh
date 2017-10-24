#!/bin/bash
set -e

sudo gunicorn --reload -b 127.0.1.2:80 q:read
