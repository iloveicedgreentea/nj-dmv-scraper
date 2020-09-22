SHELL := /usr/bin/env bash

APP_NAME := dmv-api

.PHONY: all

all: build

build:
	docker build -t $(APP_NAME) .

run:
	@mkdir output &> /dev/null || true
	@echo
	@echo
	@docker run -it -v '$(PWD)/output:/app/output' "$(APP_NAME)" start
	

dev:
	docker run -it "$(APP_NAME)" bash

setup:
	python3 -m venv .venv
	source .venv/bin/activate && pip install -r src/requirements.txt
