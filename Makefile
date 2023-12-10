content = src testing

install-deps-dev:
	python3 -m pip install --user -r requirements-dev.txt
	python3 -m pip install --user -r requirements.txt

install-deps:
	python3 -m pip install --user -r requirements.txt

lint:
	python3 -m flake8 ${content}

format:
	python3 -m black -l 79 ${content}

test:
	make unit

unit:
	python3 -m pytest testing/unit
