help: ## Display this current help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ General

build: ## Build the project
	@echo "Building the project..."
	docker compose build --no-cache

start: ## Start the project
	@echo "Starting the project..."
	docker compose up -d

restart: ## Restart the project
	@echo "Restarting the project..."
	docker compose restart

clean: ## Clean the project
	@echo "Cleaning the project..."
	docker compose down -v --remove-orphans

start-%: ## Start a specific service
	@echo "Starting the service $*..."
	@docker compose up -d $*

stop-%: ## Stop a specific service
	@echo "Stopping the service $*..."
	@docker compose stop $*

restart-%: ## Restart a specific service
	@echo "Restarting the service $*..."
	@docker compose restart $*