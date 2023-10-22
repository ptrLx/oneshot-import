OS := $(shell uname)

.DEFAULT_GOAL:=help
.PHONY: help
help:  ## Display this help text
	$(info oneshot-import)
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: setup
setup:  ## Setup environment
	pipenv install --dev

.PHONY: start
start:  ## Start the tool
	pipenv run python src/main.py

.PHONY: build
build:  ## Build standalone executable
ifeq ($(OS),Linux)
	pipenv run pyinstaller --onefile -w -n oneshot-import --hidden-import='PIL._tkinter_finder' src/main.py
endif

ifeq ($(OS),Darwin)
	pipenv run pyinstaller --onefile -w -n oneshot-import --hidden-import='PIL._tkinter_finder' src/main.py # todo --icon logo/v1/icon.iconset
	cd ./dist/ && zip -r9 oneshot-import oneshot-import.app
endif

ifeq ($(OS),Windows)
	pipenv run pyinstaller --onefile -w -n oneshot-import --hidden-import='PIL._tkinter_finder' --icon logo/v1/icon.ico --distpath=./dist src/main.py
endif

convert-icon: ## Convert icon.svg to .ico and iconset
	cd logo/v1 && ./converter.sh