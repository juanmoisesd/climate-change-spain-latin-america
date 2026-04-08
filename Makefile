.PHONY: setup test run

setup:
	pip install -r requirements.txt

test:
	python3 -m unittest discover tests

run:
	jupyter notebook notebooks/01_quickstart.ipynb
