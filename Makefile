.PHONY: build
build:
	docker-compose build

.PHONY: start
start:
	docker-compose up -d

.PHONY: stop
stop:
	docker-compose down

.PHONY: format
format:
	black . && isort .

.PHONY: tests
tests:
	docker exec -it notification_api pytest -s
