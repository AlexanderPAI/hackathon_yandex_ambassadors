# hackathon_yandex_ambassadors
Backend CRM Yandex ambassadors

![Static Badge](https://img.shields.io/badge/status-in_progress-yellow) 
![main workflow](https://github.com/AlexanderPAI/hackathon_yandex_ambassadors/actions/workflows/main.yaml/badge.svg)
![Static Badge](https://img.shields.io/badge/Python-FFD43B?logo=python&logoColor=blue) 
![Static Badge](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=green)
![Static Badge](https://img.shields.io/badge/JWT-000000?logo=JSON%20web%20tokens&logoColor=white)
![Static Badge](https://img.shields.io/badge/Google%20Sheets-34A853?logo=google-sheets&logoColor=white)
![Static Badge](https://img.shields.io/badge/Swagger-85EA2D?logo=Swagger&logoColor=white)
![Static Badge](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white)
![Static Badge](https://img.shields.io/badge/Docker-2CA5E0?logo=docker&logoColor=white) 
![Static Badge](https://img.shields.io/badge/Nginx-009639?logo=nginx&logoColor=white) 
![Static Badge](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)

# Описание проекта

# Команда backend разработки

- [AlexanderPAI](https://github.com/AlexanderPAI) - тимлид, руководство командой
backend-разработки, code review, разработка эндпойнтов гайдов и контента амбассадоров
(эндпойнты guide_kits, guide_tasks, guides)
- [earlinn](https://github.com/earlinn) - разработка эндпойнтов мерча, заявок на мерч,
промокодов амбассадоров, годового бюджета (эндпойнты merch_category, merch_price,
promocodes, send_merch); настройка динамической документации апи в форматах Swagger и
Redoc; деплой на сервер и настройка CI/CD; настройка интеграции с Google Sheets API
- [IlyaKotenko](https://github.com/IlyaKotenko) - разработка эндпойнтов создания,
редактирования, удаления и просмотра информации об амбассадорах (эндпойнты ambassadors);
настройка интеграции с Яндекс Формами для регистрации новых амбассадоров
- [mspitsyn](https://github.com/mspitsyn) - разработка эндпойнтов пользователей с
авторизацией по JWT-токенам (эндпойнты auth), настройка логирования действий юзеров
через LogEntry (эндпойнты edit_history)

# Динамически генерируемая документация апи

Чтобы посмотреть динамическую документацию апи, нужно запустить приложение и
пройти по одной из этих ссылок:
- в формате Swagger - http://127.0.0.1:8000/api/v1/swagger/
- в формате Redoc - http://127.0.0.1:8000/api/v1/redoc/

# Запуск проекта на локальном компьютере

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AlexanderPAI/hackathon_yandex_ambassadors.git
cd hackathon_yandex_ambassadors
```

Создать в папке hackathon_yandex_ambassadors/src/config файл с названием ".env" и следующим 
содержанием:

```
SECRET_KEY = <вписать секретный ключ>
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env

# для Linux
source env/bin/activate

# для Windows
env\Scripts\activate
# в случае с терминалом bash эта команда может не сработать, тогда следует 
перейти в папку Scripts командой
cd env/Scripts/
# и активировать виртуальное окружение, поставив впереди точку:
. activate

# деактивировать виртуальное окружение можно командой
deactivate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Создать суперпользователя с правами администратора:

```
python3 manage.py createsuperuser
```

Локально запустить проект из папки api_final_yatube/yatube_api/:

```
python3 manage.py runserver
```

Выйти из проекта: Ctrl + C.
