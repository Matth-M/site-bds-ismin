FRONT_END_DIR=client

PNPM=pnpm

# Front end commands

front-dev: $(FRONT_END_DIR)
	$(PNPM) -C $(FRONT_END_DIR) run dev

$(FRONT_END_DIR):
	mkdir -p $@
