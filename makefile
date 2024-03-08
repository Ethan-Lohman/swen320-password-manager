.PHONY: install run

install:
	pip install -r requirements.txt

run:
	python -m dotenv run python manage.py run -p 8080