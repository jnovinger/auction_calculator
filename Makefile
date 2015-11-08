.PHONY: clean clean-pyc clean-build docs manage runserver

export SHELL := /bin/bash

PROJECT ?= auction_calculator
export PROJECT

# config locations
REQUIREMENTS := requirements.txt
DEV_REQUIREMENTS := requirements/dev.txt
REQ_FILES := $(REQUIREMENTS) $(DEV_REQUIREMENTS)

# precomputes
PWD := $(shell pwd)/
GIT_BRANCH := $(shell git branch | grep "*" | cut -d " " -f 2)
CACHE_BUSTER := $(shell date +%Y%m%d%H%M%S)
DATE := $(CACHE_BUSTER)
DB_NAME ?= auction
DB_TEMPLATE ?= template0
HEROKU_APP ?= auction_calculator

# command aliases
VIRTUAL_ENV ?= $(WORKON_HOME)/$(PROJECT)
BIN := $(VIRTUAL_ENV)/bin
PIP := $(BIN)/pip
PYTHON := $(BIN)/python
PYLINT := $(BIN)/pylint
WHEEL_DIR := $(HOME)/.pip/wheels/
BIN_DIR := bin
MANAGEPY := $(BIN_DIR)/manage.py

PG_DUMP := $(shell which pg_dump)
PG_RESTORE := $(shell which pg_restore)
DROPDB := $(shell which dropdb)
CREATEDB := $(shell which createdn)


BACKUP_DIR := backups
DB_BAK_FILE := $(BACKUP_DIR)/$(shell test -d $(BACKUP_DIR) && ls -t $(BACKUP_DIR)/ | grep "$(DB_NAME)" -m 1 | cut -d " " -f 10)

# env setup related
PIP_INSTALL_ARGS =

FORCE:

mkvenv:
	@echo "Checking if the $(PROJECT) virtualenv exists ..."
	test -d $(VIRTUAL_ENV) || $(MAKE) _mkvenv $(MAKE) update_tools

_mkvenv:
	@echo "Creating the $(PROJECT) virtual env ..."
	source /usr/local/bin/virtualenvwrapper.sh && \
	mkvirtualenv $(PROJECT)

update_tools:
	$(PIP) install --upgrade pip wheel setuptools

update_reqs:
	$(PIP) install --upgrade -r requirements.txt -r requirements/dev.txt

_create_backup_dir:
	test -d $(BACKUP_DIR) || mkdir $(BACKUP_DIR)

dump_db: _create_backup_dir
	$(PG_DUMP) -Fc -f "$(BACKUP_DIR)/$(DB_NAME)_$(DATE).dump"

# snapshot.dump: _create_backup_dir
# 	wget -O $(BACKUP_DIR)/$(DB_NAME)_$(DATE).dump `heroku pg:backups public-url -q --app $(HEROKU_APP)`
# 
create_db_bak:
	createdb $(DB_NAME)-local-back-$(DATE) -T $(DB_NAME)

restore_dump:
	-$(DROPDB) $(DB_NAME)
	$(CREATEDB) $(DB_NAME) -T $(DB_TEMPLATE)
	-$(PG_RESTORE) --verbose --clean --no-acl --no-owner -j 3 -d $(DB_NAME) $(DB_BAK_FILE)
# 
# get_db_from_prod: snapshot.dump create_db_bak restore_dump


$(REQ_FILES): FORCE
	@echo "Installing $@ requirements file ..."
	$(PIP) install $(PIP_INSTALL_ARGS) -r $@

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean: clean-build clean-pyc clean-pycache clean-test clean-vim

clean-build:
	-rm -fr build/
	-rm -fr dist/
	-rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-pycache:
	find . -iname "__pycache__" -exec rm -rf {} +

clean-test:
	-rm .coverage
	-rm nosetests.xml
	-rm -rf cover/

clean-vim:
	find . -name '*.swp' -exec rm -f {} +
	find . -name '*.swo' -exec rm -f {} +

lint:
	flake8 $(LINT_TARGETS)

test:
	$(PYTHON) $(MANAGEPY) test

test-fast:
	$(PYTHON) $(MANAGEPY) test --failfast 2>&1 | ts

coverage:
	coverage run --source $(COVERAGE_TARGETS)
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/dailydot.com.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ .
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

runserver:
	$(PYTHON) $(MANAGEPY) runserver 0:8000

# If the first argument is "run"...
# adapted from http://stackoverflow.com/a/14061796/106765
ifeq (manage,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

manage:
	$(PYTHON) $(MANAGEPY) ${RUN_ARGS}

print-%: ; @echo $*=$($*)

echo-%: ; @echo $($*)
