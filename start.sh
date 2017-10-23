#!/bin/bash

set -e
sudo gunicorn --reload -b 0.0.0.0:80 q:read
