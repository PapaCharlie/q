# All of the following variables are overriden by ennvironment variables
Q_DIR ?= /var/tmp/q
Q_SHORTCUTS_FILE ?= $(shell echo ~/.q.yaml)
Q_SHORTCUTS_LOCK ?= $(Q_DIR)/shortcuts_lock
Q_LOOPBACK_IP ?= 127.0.1.2

all: start

start:
	mkdir -p $(Q_DIR)
	test -e $(Q_DIR)/q.pid && echo "q is already running!" && exit 1 || true
	sudo gunicorn \
		--daemon \
		--pid $(Q_DIR)/q.pid \
		--access-logfile $(Q_DIR)/q.access \
		--log-file $(Q_DIR)/q.log \
		--workers 4 \
		--reload \
		--bind $(LOOPBACK_IP):80 \
		--env SHORTCUTS="$(Q_SHORTCUTS_FILE)" \
		--env SHORTCUTS_LOCK="$(Q_SHORTCUTS_LOCK)" \
		q:read

loopback-alias:
	sudo ifconfig lo0 alias $(LOOPBACK_IP)

kill:
	sudo kill $(shell cat $(Q_DIR)/q.pid)

ps:
	pgrep -f gunicorn | xargs ps

log:
	tail -F $(Q_DIR)/q.log
