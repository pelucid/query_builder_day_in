venv:
ifndef VIRTUAL_ENV
ifndef CONDA_PREFIX
$(error VIRTUAL / CONDA ENV is not set - please activate environment)
endif
endif

run: venv
	PYTHONPATH=${PWD}/../:${PYTHONPATH} python main.py

deps: venv
	pip install -Ur requirements.txt

test: venv
	pytest -svv tests/
