# DOCKER TASKS

rundev: ## Run container in development mode
	@docker-compose -f docker-compose-dev.yml up

runstaging: ## Run container in stage mode
	@docker-compose -f docker-compose-staging.yml up
