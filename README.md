# hackathon_yandex_ambassadors
Backend CRM Yandex ambassadors

![Static Badge](https://img.shields.io/badge/status-in_progress-yellow) 
![main workflow](https://github.com/AlexanderPAI/hackathon_yandex_ambassadors/actions/workflows/main.yaml/badge.svg)

# Описание проекта

# Команда backend разработки

имя - роль (в виде ссылки на ГитХаб)

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
