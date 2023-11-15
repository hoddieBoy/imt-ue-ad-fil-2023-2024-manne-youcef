help: ## Display this current help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ General

.PHONY: build start

build: ## Build the project
    @echo "Building the project..."
    @docker compose build

start: ## Start the project
    @echo "Starting the project..."
    @docker compose up -d

stop: ## Stop the project
    @echo "Stopping the project..."
    @docker compose down

reload: stop start ## Reload the project
    @echo "Reloading the project..."

## Reload a specific service
reload-%: ## Reload a specific service
    @echo "Reloading the project..."
    @docker compose restart $*

