run:
	cd src; python3 manage.py runserver

makemig:
	cd src; python3 manage.py makemigrations

makemig-ambassadors:
	cd src; python3 manage.py makemigrations ambassadors

makemig-content:
	cd src; python3 manage.py makemigrations content

makemig-promo:
	cd src; python3 manage.py makemigrations promo

makemig-users:
	cd src; python3 manage.py makemigrations users

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

dumpdb:
	cd src; python3 manage.py dumpdata --output dump.json

loaddb:
	cd src; python3 manage.py loaddata dump.json

collectstatic:
	cd src; python3 manage.py collectstatic --no-input

up-compose:
	sudo docker compose -f docker-compose.local.yml up -d

build-compose:
	sudo docker compose -f docker-compose.local.yml up -d --build

stop-compose:
	sudo docker compose -f docker-compose.local.yml stop

start-compose:
	sudo docker compose -f docker-compose.local.yml start

makemig-compose:
	sudo docker compose -f docker-compose.local.yml exec -it backend python manage.py makemigrations

migrate-compose:
	sudo docker compose -f docker-compose.local.yml exec -it backend python manage.py migrate

superuser-compose:
	sudo docker compose -f docker-compose.local.yml exec -it backend python manage.py createsuperuser --email test@test.com --username admin -v 3

collectstatic-compose:
	sudo docker compose -f docker-compose.local.yml exec -it backend python manage.py collectstatic --no-input

shell-compose:
	sudo docker compose -f docker-compose.local.yml exec -it backend python manage.py shell

ls-compose:
	sudo docker compose -f docker-compose.local.yml exec -it backend ls

prune-containers:
	sudo docker container prune

prune-images:
	sudo docker image prune
