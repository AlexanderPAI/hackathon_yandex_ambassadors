import pytest
from rest_framework.test import APIClient

from ambassadors.models import Activity, Address, Ambassador, Program, Purpose, Status
from promo.models import Merch, MerchCategory, Promocode
from users.models import User

TEST_NAME = "Test"
TEST_SIZE = "XXS"
TEST_SLUG = "test-test-test"
TEST_COST = 1000
TEST_PAST_DATETIME = "2020-03-04T16:20:55+03:00"

USER = "test_user"
USER_EMAIL = "test_user@test.com"
ADMIN = "TestAdmin"
ADMIN_EMAIL = "testadmin@good_food.fake"
PASSWORD = "test_password"
ADDRESS = "Test address"

ADDRESS_POSTAL_CODE_1 = 111111
ADDRESS_POSTAL_CODE_2 = 222222
ADDRESS_POSTAL_CODE_3 = 333333
ADDRESS_COUNTRY = "Россия"
ADDRESS_CITY = "Москва"
ADDRESS_STREET_1 = "Улица 1"
ADDRESS_STREET_2 = "Улица 2"
ADDRESS_STREET_3 = "Улица 3"

ACTIVITY_1 = "вести блог"
ACTIVITY_2 = "знакомить коллег с ЯП"
ACTIVITY_3 = "Писать статьи"

PURPOSE_1 = "сменить работу"
PURPOSE_2 = "подтянуть знания"

PROGRAM_1 = "Python-разработчик"
PROGRAM_2 = "Web-разработчик"
PROGRAM_3 = "Бизнес-аналитик"

STATUS_1 = "активный"
STATUS_2 = "уточняется"

AMBASSADOR_NAME_1 = "Петя Вектор"
AMBASSADOR_NAME_2 = "Соня Васькина"
AMBASSADOR_NAME_3 = "Макар Макарыч"
AMBASSAGOR_GENDER_1 = "Ж"
AMBASSAGOR_GENDER_2 = "М"
AMBASSADOR_SHOE_SIZE_1 = "42"
AMBASSADOR_SHOE_SIZE_2 = "38"
AMBASSADOR_SHOE_SIZE_3 = "40"
AMBASSADOR_CLOTHING_SIZE_1 = "L"
AMBASSADOR_CLOTHING_SIZE_2 = "S"
AMBASSADOR_CLOTHING_SIZE_3 = "M"
AMBASSADOR_EDUCATION_1 = "МГУ"
AMBASSADOR_EDUCATION_2 = "СПБГУ"
AMBASSADOR_EDUCATION_3 = "ВГУ"
AMBASSADOR_JOB_1 = "логгист"
AMBASSADOR_JOB_2 = "таксист"
AMBASSADOR_JOB_3 = "продавец"
AMBASSADOR_EMAIL_1 = "petya@test.com"
AMBASSADOR_EMAIL_2 = "sonya@test.com"
AMBASSADOR_EMAIL_3 = "makar@test.com"
AMBASSADOR_PHONE_1 = "88002222222"
AMBASSADOR_PHONE_2 = "88003333333"
AMBASSADOR_PHONE_3 = "88004444444"
AMBASSADOR_TELEGRAM_1 = "@petya"
AMBASSADOR_TELEGRAM_2 = "@sonya"
AMBASSADOR_TELEGRAM_3 = "@makar"

PROMOCODE_1 = "3hhlk72"
PROMOCODE_2 = "fjg657454"
PROMOCODE_3 = "dhfu6k12121"
PROMOCODE_4 = "565667k"

CATEGORY_1 = "толстовка"
CATEGORY_2 = "футболка"
CATEGORY_3 = "носки"

MERCH_NAME_1 = "Футболка с логотипом Яндекса черная"
MERCH_NAME_2 = "Футболка с логотипом Яндекса белая"
MERCH_NAME_3 = "Толстовка красная женская"
MERCH_NAME_4 = "Толстовка синяя"
MERCH_NAME_5 = "Носки VSCode"
MERCH_NAME_6 = "Носки PyCharm"
MERCH_SIZE_1 = "S"
MERCH_SIZE_2 = "L"
MERCH_SIZE_3 = "M"
MERCH_SIZE_4 = "S"
MERCH_SIZE_5 = "39-40"
MERCH_SIZE_6 = "41-42"
MERCH_COST_1 = 300
MERCH_COST_2 = 350
MERCH_COST_3 = 560
MERCH_COST_4 = 550
MERCH_COST_5 = 240
MERCH_COST_6 = 365


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_user(
        username=ADMIN, email=ADMIN_EMAIL, password=PASSWORD, is_staff=True
    )


@pytest.fixture
def user():
    return User.objects.create_user(username=USER, email=USER_EMAIL, password=PASSWORD)


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_client(client, user):
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def auth_admin(client, admin):
    client.force_authenticate(user=admin)
    return client


@pytest.fixture
def addresses():
    Address.objects.create(
        postal_code=ADDRESS_POSTAL_CODE_1,
        country=ADDRESS_COUNTRY,
        city=ADDRESS_CITY,
        street=ADDRESS_STREET_1,
    )
    Address.objects.create(
        postal_code=ADDRESS_POSTAL_CODE_2,
        country=ADDRESS_COUNTRY,
        city=ADDRESS_CITY,
        street=ADDRESS_STREET_2,
    )
    Address.objects.create(
        postal_code=ADDRESS_POSTAL_CODE_3,
        country=ADDRESS_COUNTRY,
        city=ADDRESS_CITY,
        street=ADDRESS_STREET_3,
    )
    return Address.objects.all()


@pytest.fixture
def activities():
    Activity.objects.create(name=ACTIVITY_1)
    Activity.objects.create(name=ACTIVITY_2)
    Activity.objects.create(name=ACTIVITY_3)
    return Activity.objects.all()


@pytest.fixture
def purposes():
    Purpose.objects.create(name=PURPOSE_1)
    Purpose.objects.create(name=PURPOSE_2)
    return Purpose.objects.all()


@pytest.fixture
def programs():
    Program.objects.create(name=PROGRAM_1)
    Program.objects.create(name=PROGRAM_2)
    Program.objects.create(name=PROGRAM_3)
    return Program.objects.all()


@pytest.fixture
def statuses():
    Status.objects.create(name=STATUS_1)
    Status.objects.create(name=STATUS_2)
    return Status.objects.all()


@pytest.fixture
def ambassadors(addresses, activities, purposes, programs, statuses):
    petya = Ambassador.objects.create(
        name=AMBASSADOR_NAME_1,
        gender=AMBASSAGOR_GENDER_1,
        clothing_size=AMBASSADOR_CLOTHING_SIZE_1,
        shoe_size=AMBASSADOR_SHOE_SIZE_1,
        education=AMBASSADOR_EDUCATION_1,
        job=AMBASSADOR_JOB_1,
        email=AMBASSADOR_EMAIL_1,
        phone_number=AMBASSADOR_PHONE_1,
        telegram_id=AMBASSADOR_TELEGRAM_1,
        purpose=purposes[0],
        program=programs[0],
        status=statuses[0],
        address=addresses[0],
    )
    petya.activity.set(activities)
    sonya = Ambassador.objects.create(
        name=AMBASSADOR_NAME_2,
        gender=AMBASSAGOR_GENDER_2,
        clothing_size=AMBASSADOR_CLOTHING_SIZE_2,
        shoe_size=AMBASSADOR_SHOE_SIZE_2,
        education=AMBASSADOR_EDUCATION_2,
        job=AMBASSADOR_JOB_2,
        email=AMBASSADOR_EMAIL_2,
        phone_number=AMBASSADOR_PHONE_2,
        telegram_id=AMBASSADOR_TELEGRAM_2,
        purpose=purposes[0],
        program=programs[1],
        status=statuses[0],
        address=addresses[1],
    )
    sonya.activity.set(activities[:2])
    makar = Ambassador.objects.create(
        name=AMBASSADOR_NAME_3,
        gender=AMBASSAGOR_GENDER_1,
        clothing_size=AMBASSADOR_CLOTHING_SIZE_3,
        shoe_size=AMBASSADOR_SHOE_SIZE_3,
        education=AMBASSADOR_EDUCATION_3,
        job=AMBASSADOR_JOB_3,
        email=AMBASSADOR_EMAIL_3,
        phone_number=AMBASSADOR_PHONE_3,
        telegram_id=AMBASSADOR_TELEGRAM_3,
        purpose=purposes[1],
        program=programs[2],
        status=statuses[1],
        address=addresses[2],
    )
    makar.activity.set(activities[1:])
    return Ambassador.objects.all()


@pytest.fixture
def promocodes(ambassadors):
    Promocode.objects.create(code=PROMOCODE_1, ambassador=ambassadors[0])
    Promocode.objects.create(code=PROMOCODE_2, ambassador=ambassadors[0])
    Promocode.objects.create(code=PROMOCODE_3, ambassador=ambassadors[1])
    Promocode.objects.create(
        code=PROMOCODE_4, ambassador=ambassadors[2], is_active=False
    )
    return Promocode.objects.all()


@pytest.fixture
def merch_categories():
    MerchCategory.objects.create(name=CATEGORY_1)
    MerchCategory.objects.create(name=CATEGORY_2)
    MerchCategory.objects.create(name=CATEGORY_3)
    return MerchCategory.objects.all()


@pytest.fixture
def merch(merch_categories):
    Merch.objects.create(
        name=MERCH_NAME_1,
        category=merch_categories[1],
        size=MERCH_SIZE_1,
        cost=MERCH_COST_1,
    )
    Merch.objects.create(
        name=MERCH_NAME_2,
        category=merch_categories[1],
        size=MERCH_SIZE_2,
        cost=MERCH_COST_2,
    )
    Merch.objects.create(
        name=MERCH_NAME_3,
        category=merch_categories[0],
        size=MERCH_SIZE_3,
        cost=MERCH_COST_3,
    )
    Merch.objects.create(
        name=MERCH_NAME_4,
        category=merch_categories[0],
        size=MERCH_SIZE_4,
        cost=MERCH_COST_4,
    )
    Merch.objects.create(
        name=MERCH_NAME_5,
        category=merch_categories[2],
        size=MERCH_SIZE_5,
        cost=MERCH_COST_5,
    )
    Merch.objects.create(
        name=MERCH_NAME_6,
        category=merch_categories[2],
        size=MERCH_SIZE_6,
        cost=MERCH_COST_6,
    )
    return Merch.objects.all()
