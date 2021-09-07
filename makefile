# makefile

install:
	python3 -m poetry install

load:
	python3 -m poetry run page_loader
	
build:
	python3 -m poetry build
	
publish:
	python3 -m poetry publish --dry-run
	
package-install:
	python3 -m pip install --user dist/*.whl

package-install-reinstall:
	python3 -m pip install --user dist/*.whl --force-reinstall

lint:
	python3 -m poetry run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127

test:
	python3 -m poetry run pytest

extended-test:
	python3 -m poetry run pytest -vv

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml