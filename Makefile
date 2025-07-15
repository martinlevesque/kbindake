
pyright:
	pyright

test:
	PYTHONPATH=. pytest

test-watch:
	find ./ -name '*.py' | entr -d sh -c 'black . && make pyright && make test'
