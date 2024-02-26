run:
	cd src; python3 manage.py runserver

makemig:
	cd src; python3 manage.py makemigrations

migrate:
	cd src; python3 manage.py migrate

superuser:
	cd src; python3 manage.py createsuperuser --email test@test.com --username admin -v 3

superuser-empty:
	cd src; python3 manage.py createsuperuser

shell:
	cd src; python3 manage.py shell

freeze:
	pip freeze > requirements.txt
