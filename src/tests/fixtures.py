import pytest
from rest_framework.test import APIClient

from promo.models import Merch, MerchCategory
from users.models import User

TEST_NAME = "Test"
TEST_SIZE = "XXS"
TEST_SLUG = "test-test-test"
TEST_COST = 1000

USER = "test_user"
USER_EMAIL = "test_user@test.com"
ADMIN = "TestAdmin"
ADMIN_EMAIL = "testadmin@good_food.fake"
PASSWORD = "test_password"
ADDRESS = "Test address"

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
