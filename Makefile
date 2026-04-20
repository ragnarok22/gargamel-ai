PORT ?= /dev/cu.usbserial-0001
MPREMOTE = uv run mpremote connect $(PORT)

.PHONY: help run deploy repl ls reset

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

run: ## Run main.py on the device (does not save it)
	$(MPREMOTE) mount . run main.py

deploy: ## Copy all .py files to the device filesystem
	for f in *.py; do $(MPREMOTE) fs cp $$f :$$f; done

repl: ## Open an interactive MicroPython REPL
	$(MPREMOTE) repl

ls: ## List files on the device filesystem
	$(MPREMOTE) fs ls

reset: ## Soft-reset the device
	$(MPREMOTE) reset
