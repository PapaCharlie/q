Q_DIR = /var/tmp/q
SHORTCUTS = $(shell echo ~/.q.yaml)
SHORTCUTS_LOCK = $(Q_DIR)/shortcuts_lock
LOOPBACK_IP = 127.0.1.2

loopback-alias:
	sudo ifconfig lo0 alias $(LOOPBACK_IP)

start:
	mkdir -p $(Q_DIR)
	sudo gunicorn \
		--daemon \
		--pid $(Q_DIR)/q.pid \
		--access-logfile $(Q_DIR)/q.access \
		--log-file $(Q_DIR)/q.log \
		--workers 4 \
		--reload \
		--bind $(LOOPBACK_IP):80 \
		--env SHORTCUTS="$(SHORTCUTS)" \
		--env SHORTCUTS_LOCK="$(SHORTCUTS_LOCK)" \
		q:read

kill:
	sudo kill $(shell cat $(Q_DIR)/q.pid)

ps:
	pgrep -f gunicorn | xargs ps

log:
	tail -F $(Q_DIR)/q.log
