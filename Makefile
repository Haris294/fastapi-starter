run:        ## dev server in Docker
	docker compose up --build
up:         ## start detached
	docker compose up -d
down:       ## stop containers
	docker compose down
logs:       ## tail logs
	docker compose logs -f
ps:         ## show services
	docker compose ps
test:       ## run tests locally
	pytest -q
lint:       ## format & lint
	python -m pip install -U black ruff >/dev/null && black . && ruff .
dbshell:    ## psql into dev DB
	docker compose exec db psql -U app -d app
shell:      ## shell in API container
	docker compose exec api sh
