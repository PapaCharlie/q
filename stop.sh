#!/bin/bash
set -e

TMPDIR=/var/tmp/q

sudo kill $(cat $TMPDIR/q.pid)
