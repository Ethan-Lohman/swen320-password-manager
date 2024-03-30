.PHONY: install run test setup
.PHONY: migrate

install:
	pip install -r requirements.txt

setup:
	pip install -r requirements.txt && \
	. ./.env && \
	python -m flask db migrate && \
	python -m flask db upgrade

run:
	python -m dotenv run python manage.py run -p 8080

migrate:
	python -m flask db migrate && \
	python -m flask db upgrade

test:
	python manage.py test

statement:
	coverage run -m unittest discover -v && \
	coverage report -m

branch:
	coverage run --branch -m unittest discover -v && \
	coverage report -m