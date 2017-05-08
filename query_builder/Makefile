venv:
ifndef VIRTUAL_ENV
ifndef CONDA_PREFIX
$(error VIRTUAL / CONDA ENV is not set - please activate environment)
endif
endif

deps: venv
	pip install -Ur requirements.txt

test: venv
	pytest -svv tests/
