UNAME := $(shell uname)

ifeq ($(OSTYPE), Windows_NT)
	PYTHON := python
	PIP := pip
else
	PYTHON := python3
	PIP := pip3
endif

create-env:
	$(PYTHON) -m venv venv

install-env:
ifeq ($(OSTYPE), Windows_NT)
	( \
		./venv/Scripts/activate; \
		$(PIP) install -r requirements.txt; \
	)
else ifeq ($(UNAME), Linux)
	( \
		. venv/bin/activate; \
		$(PIP) install -r requirements.txt; \
	)
else
	( \
		source venv/bin/activate; \
		$(PIP) install -r requirements.txt; \
	)
endif

install-dev-env:
ifeq ($(OSTYPE), Windows_NT)
	( \
		./venv/Scripts/activate; \
		$(PIP) install -r requirements_dev.txt; \
	)
else ifeq ($(UNAME), Linux)
	( \
		. venv/bin/activate; \
		$(PIP) install -r requirements_dev.txt; \
	)
else
	( \
		source venv/bin/activate; \
		$(PIP) install -r requirements_dev.txt; \
	)
endif

setup-dev-chatpg: create-env install-dev-env

setup-chatpg: create-env install-env

test-ci-chatpg:
ifeq ($(OSTYPE), Windows_NT)
	( \
		./venv/Scripts/activate; \
		pytest; \
	)
else ifeq ($(UNAME), Linux)
	( \
		. venv/bin/activate; \
		pytest; \
	)
else
	( \
		source venv/bin/activate; \
		pytest; \
	)
endif

test-chatpg:
ifeq ($(OSTYPE), Windows_NT)
	( \
		./venv/Scripts/activate; \
		tox; \
	)
else ifeq ($(UNAME), Linux)
	( \
		. venv/bin/activate; \
		tox; \
	)
else
	( \
		source venv/bin/activate; \
		tox; \
	)
endif
