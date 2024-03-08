# hackathon_yandex_ambassadors
![Static Badge](https://img.shields.io/badge/status-in_progress-yellow)
![main workflow](https://github.com/AlexanderPAI/hackathon_yandex_ambassadors/actions/workflows/main.yaml/badge.svg)   
Backend CRM Yandex ambassadors - внутренняя CRM система. 
Пространство для комьюнити менеджера сообщества амбассадоров, в котором можно получать уведомления, делать рассылки и смотреть аналитику.


## Основной функционал CRM системы:  
Хранение данных с возможность редактирования и работы с ними (настроенная интеграция с Я Формами)  
·	Вся информация по амбассадорам из формы  
·	Промокоды  
·	Контент  
·	Программа лояльности  
·	Отправка мерча  
·	Бюджет на мерч  

## Сведения о команде 
Менеджер проекта - отвечает за синхронизацию Команды, выполнение задач в дедлайны Конкурса и организационные вопросы:   
Артем Криуков https://t.me/artem_kriukov 
    
Product-менеджер – делает: анализ ЦА, прописывает цели, задачи проекта, гипотезы, юзерфлоу (как ни странно, неправда ли), юзерстори, портрет пользователя, рисует макет MVP:     
Ксения https://t.me/kseniturina 
 
SA – отвечает за технические требования:   
Александр Жолков https://t.me/oozebourne  
Артем Джага https://t.me/purple_SU  
Игорь Савельев https://t.me/IgorS1306  
  
BA – отвечает за бизнес требования:   
Sve Ti https://t.me/Sve999Ti  
Маргарита  https://t.me/MargaritaAVT  
 
Дизайнер — креативщик Команды, отвечает за UI/UX, дизайн макетов:    
Антонина Балашова https://t.me/Antonina_Balashova   
Екатерина https://t.me/glodeva  
Мурат Дауров https://t.me/mura_murik  
 
Frontend-разработчик – отвечает за визуализацию данных:    
Анастасия Нистратова https://t.me/Anastasia_Niii  
Денис https://t.me/DezmonDND  
Дарья Соколова https://t.me/dariryzhaya  
 
Backend-разработчик – отвечает за обработку данных:   
Александр https://t.me/alex_mw   
Ear Lin https://t.me/Earlinn   
Илья Котенко https://t.me/IlyaKotenko  
Максим Спицын https://t.me/maxu_s  
 
## Динамически генерируемая документация апи 
 
Чтобы посмотреть динамическую документацию апи, нужно запустить приложение и
пройти по одной из этих ссылок: 
- в формате Swagger - http://127.0.0.1:8000/api/v1/swagger/  
- в формате Redoc - http://127.0.0.1:8000/api/v1/redoc/  
 
 
## Стэк технологий   
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)

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
