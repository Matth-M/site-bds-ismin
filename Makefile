## Change for your preferences
VENV=env
APP=website

# VIRTUAL ENVIRONMENT
VENV_CLI=venv
VENV_BIN_DIR=$(VENV)/bin

REQUIREMENTS=requirements.txt

PIP=$(VENV_BIN_DIR)/pip

## VIRTUAL ENVIRONMENT

$(VENV):
	python3 -m $(VENV_CLI) $(VENV)
	@$(PIP) install -r $(REQUIREMENTS)

.PHONY: freeze
freeze: $(VENV)
	$(PIP) freeze > $(REQUIREMENTS)
	@echo "Requirements updated"

.PHONY: show-requirements
show-requirements:
	@cat $(REQUIREMENTS)

.PHONY: clean
clean:
	@rm -rf .cache
	@rm -rf htmlcov coverage.xml .coverage
	@find . -name *.pyc -delete
	@find . -name db.sqlite3 -delete
	@find . -type d -name __pycache__ -delete
	@rm -rf venv
	@rm -rf .tox


# start development server
.PHONY: dev-server
dev-server: $(VENV)
	$(VENV_BIN_DIR)/flask --app $(APP) run
