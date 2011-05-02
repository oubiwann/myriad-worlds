clean:
	find -name "*.pyc" -exec rm {} \;
	find -name "*.pyo" -exec rm {} \;

test:
	python myrolds/testing/runner.py

check: test
