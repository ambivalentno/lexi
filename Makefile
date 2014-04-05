# -*- makefile -*-

# definitions
PROJECT       = lexi
HOST          = 127.0.0.1
PORT          = 8000
CURRPATH      = $(shell pwd)
PIDFILE       = $(shell pwd)/etc/django.pid


PROJECT_TEST_TARGETS=lection users

# constants
PYTHONPATH = .:..
PYTHON     = python

MANAGE=cd $(PROJECT) && PYTHONPATH=$(PYTHONPATH) DJANGO_SETTINGS_MODULE=$(PROJECT).settings django-admin.py

# end

run:
	$(MAKE) clean
	$(MANAGE) runserver $(HOST):$(PORT)

syncdb:
	$(MAKE) clean
	$(MANAGE) syncdb --noinput
	$(MAKE) manage -e CMD="migrate"

fresh_syncdb:
	-rm dev.db
	$(MANAGE) syncdb --noinput
	$(MAKE) manage -e CMD="migrate"
	@echo Loading initial fixtures...
	$(MANAGE) loaddata base_initial_data.json
	$(MANAGE) loaddata cron.json
	@echo Done

test:
	$(MAKE) clean
	TESTING=1 $(MANAGE) test $(TEST_OPTIONS) $(PROJECT_TEST_TARGETS)


clean:
	@echo Cleaning up *.pyc files
	-find . | grep '.pyc$$' | xargs -I {} rm {}

migrate:
ifndef APP_NAME
	@echo Please, specify -e APP_NAME=appname argument
else
	@echo Starting of migration of $(APP_NAME)
	-$(MANAGE) schemamigration $(APP_NAME) --auto
	$(MANAGE) migrate $(APP_NAME)
	@echo Done
endif

init_migrate:
ifndef APP_NAME
	@echo Please, specify -e APP_NAME=appname argument
else
	@echo Starting init migration of $(APP_NAME)
	$(MANAGE) schemamigration $(APP_NAME) --initial
	$(MANAGE) migrate $(APP_NAME)
	@echo Done
endif

manage:
ifndef CMD
	@echo Please, specify CMD argument to execute Django management command
else
	$(MANAGE)  $(CMD)
endif

help:
	@cat README

# production activation/deactivation
uwsgi_reload:
	touch $(CURRPATH)/etc/reload.txt

uwsgi:
	uwsgi --socket $(HOST):$(PORT) --chdir $(CURRPATH) --pp $(PROJECT) -w $(PROJECT).wsgi --virtualenv=$(CURRPATH)/.env --pidfile=$(PIDFILE) --daemonize $(CURRPATH)/logs/uwsgi.log --touch-reload=$(CURRPATH)/etc/reload.txt -b 32768
	@echo "uwsgi on $(CURRPATH):$(PORT) started"

uwsgi_stop:
	uwsgi --stop $(PIDFILE)

shell:
	$(MAKE) clean
	$(MANAGE) shell_plus

dbshell:
	$(MAKE) clean
	$(MANAGE) dbshell
