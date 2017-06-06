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
	python manage.py runserver 0.0.0.0:8000

gulp:
	gulp

ci: clean env info test
	codecov

ans_deploy:
	ansible-playbook --private-key=.vagrant/machines/default/virtualbox/private_key -u vagrant -i ansible/hosts ansible/ansible-phillydsa-com.yml -vvvv --vault-password-file ~/.vault_pass.txt

deploy:
	ansible-playbook --private-key=~/.ssh/id_rsa -u root -i ansible/hosts ansible/phillydsa-com.yml -vv --vault-password-file ~/.vault_pass.txt
