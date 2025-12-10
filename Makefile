.PHONY: help install run demo web clean

help:
	@echo "iReply - Makefile Commands"
	@echo ""
	@echo "  make install    - Install Python dependencies"
	@echo "  make web        - Start the web server (recommended for demo)"
	@echo "  make run        - Run the CLI version"
	@echo "  make demo       - Run CLI with lower threshold"
	@echo "  make clean      - Remove Python cache files"
	@echo ""

install:
	pip3 install -r requirements.txt

web:
	@echo "Starting iReply web server..."
	@echo "Open http://localhost:8000 in your browser"
	python3 web_app.py

run:
	python3 main.py

demo:
	@echo "Running with 24h threshold for demo..."
	STALE_THRESHOLD_HOURS=24 python3 main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
