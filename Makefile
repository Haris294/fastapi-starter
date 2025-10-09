.PHONY: up down logs ps test fmt lint migrate rev

up:          ## build & start
\tdocker compose up -d --build

down:        ## stop & remove
\tdocker compose down

logs:        ## tail API logs
\tdocker compose logs -f api

ps:          ## list services
\tdocker compose ps

test:        ## run test suite in container
\tdocker compose exec api sh -lc 'pip install -q -r requirements-dev.txt || true; pytest -q'

fmt:         ## black + ruff --fix in container
\tdocker compose exec api sh -lc 'pip install -q black ruff; black . && ruff check . --fix'

lint:        ## ruff check only
\tdocker compose exec api sh -lc 'pip install -q ruff; ruff check .'

migrate:     ## run alembic migrations
\tdocker compose exec api alembic upgrade head

rev:         ## make new migration: make rev m="your message"
\tdocker compose exec api alembic revision --autogenerate -m "$(m)"
