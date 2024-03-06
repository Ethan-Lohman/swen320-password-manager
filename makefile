.PHONY: install run

install:
	pip install -r requirements.txt

run:
	dotenv run python manage.py run -p 8081