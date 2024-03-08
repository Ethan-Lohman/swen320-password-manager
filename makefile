.PHONY: install run
.PHONY: migrate

install:
	pip install -r requirements.txt

run:
	python -m dotenv run python manage.py run -p 8080

migrate:
	python -m flask db migrate && \
	python -m flask db upgrade
