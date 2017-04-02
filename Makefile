info:
	@python --version
	@pyenv --version
	@pip --version

clean:
	rm -fr build
	rm -fr dist
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' ! -name '*.un~' -exec rm -f {} \;

lint:
	pre-commit run -a

test:
	pytest

dev:
	pyenv install -s 3.6.0
	pyenv virtualenv 3.6.0 phillydsa
	pyenv local philly-dsa-membership
	pip install -r requirements/dev.txt
	pre-commit install
