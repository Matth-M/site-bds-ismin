## Change for your preferences
VENV=env
APP=website
INIT_DB_CMD=init_db


# Path

ROOT_DIR=.

APP_DIR=$(ROOT_DIR)/$(APP)

STATIC_DIR=$(APP_DIR)/static
SASS_DIR=$(APP_DIR)/scss
SASS_ENTRY=$(SASS_DIR)/main.scss

# VIRTUAL ENVIRONMENT
VENV_CLI=venv
VENV_BIN_DIR=$(VENV)/bin

REQUIREMENTS=requirements.txt


# Binary
SASS=pnpm sass
PIP=$(VENV_BIN_DIR)/pip --require-virtualenv

## VIRTUAL ENVIRONMENT

$(VENV):
	python3 -m $(VENV_CLI) $(VENV)
	@$(PIP) install -r $(REQUIREMENTS)

.PHONY: add-packages
add-packages: $(VENV) freeze
	@read -p "packages? : " PACK \
	&& $(PIP) install $${PACK}

.PHONY: remove-packages
remove-packages: $(VENV) freeze
	@read -p "packages? : " PACK \
	&& $(PIP) uninstall --yes $${PACK}

.PHONY: freeze
freeze: $(VENV)
	$(PIP) freeze > $(REQUIREMENTS)
	@echo "Requirements updated"

.PHONY: show-requirements
show-requirements:
	@cat $(REQUIREMENTS)



### DEVELOPMENT
# start development server
.PHONY: dev-server
dev-server: $(VENV)
	$(VENV_BIN_DIR)/flask --app $(APP) --debug run

# Clear the existing data and create new tables
.PHONY: init-db
init-db: $(VENV)
	$(VENV_BIN_DIR)/flask --app $(APP) $(INIT_DB_CMD)

.PHONY: sass-watch
sass-watch: $(SASS_DIR)
	$(SASS) --watch $(SASS_DIR):$(STATIC_DIR) # $(STATIC_DIR)/index.css

$(SASS_DIR):
	@mkdir -p $@




.PHONY: clean
clean:
	@rm -rf .cache
	@rm -rf htmlcov coverage.xml .coverage
	@find . -name *.pyc -delete
	@find . -name *.sqlite3 -delete
	@find . -type d -name __pycache__ -delete
	@rm -rf $(VENV)
	@rm -rf .tox
	@rm -rf $(ROOT_DIR)/instance
