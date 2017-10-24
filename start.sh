#!/bin/bash
set -e

TMPDIR=/var/tmp/q
SHORTCUTS=${1-~/.q.yaml}

mkdir -p $TMPDIR
sudo gunicorn --daemon --pid $TMPDIR/q.pid --access-logfile $TMPDIR/q.access --log-file $TMPDIR/q.log --workers 4 --reload -b 127.0.1.2:80 --env SHORTCUTS="$SHORTCUTS" q:read
