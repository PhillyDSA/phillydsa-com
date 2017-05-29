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
	pytest --cov
	coverage html

env:
	pyenv install -s 3.6.0
	pyenv local 3.6.0

install:
	pip install -Ur requirements/dev.txt

dev:
	pyenv install -s 3.6.0
	# Make will continue here in the event that the virtualenv already exists
	- pyenv virtualenv 3.6.0 phillydsa
	pyenv local phillydsa
	pip install -r requirements/dev.txt
	pre-commit install

server:
	python manage.py runserver 127.0.0.1:8000

gulp:
	gulp

ci: clean env info test
	codecov
