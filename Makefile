.PHONY: dev stop share unshare build test test-api test-e2e db-up db-down audio content

dev:
	./scripts/dev.sh

stop:
	./scripts/stop.sh

share:
	./scripts/share.sh

unshare:
	./scripts/share.sh stop

build:
	pnpm --dir apps/web build
	cd services/api && go build ./...

test: test-api test-e2e

test-api:
	cd services/api && go test ./...

test-e2e:
	cd apps/web && pnpm exec playwright test

db-up:
	docker compose up -d postgres

db-down:
	docker compose down

content:
	node --experimental-strip-types scripts/export-content.mjs

audio:
	source .venv-kokoro/bin/activate && python scripts/generate-kokoro-audio.py
