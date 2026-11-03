.PHONY: install test lint run-api demo

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

lint:
	ruff check src tests
	mypy src || true

run-api:
	uvicorn capturethebug.api.app:app --reload --port 8000

demo:
	@export CTB_DB_PATH=./demo.db; \
	rm -f demo.db; \
	ctb init; \
	ctb assessment create -n "Demo Web App" -c "ACME Corp" -t https://example.com -a "Demo Analyst"; \
	ID=$$(ctb assessment list 2>/dev/null | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}' | head -1); \
	echo "Assessment ID: $$ID"; \
	ctb import nuclei samples/nuclei-sample.jsonl -a $$ID; \
	ctb import zap samples/zap-sample.json -a $$ID; \
	ctb findings -a $$ID; \
	ctb report -a $$ID --format all -o ./demo-reports; \
	echo "Demo reports in ./demo-reports"
