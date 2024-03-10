import pytest
from django.urls import reverse

from tests.fixtures import TEST_COST, TEST_NAME, TEST_SIZE, TEST_SLUG

from api.mixins import MESSAGE_ON_DELETE


@pytest.mark.django_db
def test_get_merch_list(auth_client, merch):
    response = auth_client.get(reverse("api:merch-list"))
    assert response.status_code == 200
    assert len(response.data) == 6
    assert response.data[0]["name"] == merch[0].name
    assert response.data[0]["size"] == merch[0].size
    assert response.data[0]["cost"] == merch[0].cost


@pytest.mark.django_db
def test_get_merch_fail_if_not_authenticated(client):
    response = client.get(reverse("api:merch-list"))

    assert response.status_code == 401
    assert response.data["type"] == "client_error"
    assert response.data["errors"][0]["code"] == "not_authenticated"


@pytest.mark.django_db
def test_get_merch_by_id(auth_client, merch):
    response = auth_client.get(reverse("api:merch-detail", kwargs={"pk": merch[2].pk}))

    assert response.status_code == 200
    assert response.data["name"] == merch[2].name
    assert response.data["size"] == merch[2].size
    assert response.data["cost"] == merch[2].cost


@pytest.mark.django_db
def test_create_merch(auth_client, merch_categories):
    payload = {
        "name": TEST_NAME,
        "size": TEST_SIZE,
        "cost": TEST_COST,
        "category": merch_categories[2].pk,
    }
    response = auth_client.post(reverse("api:merch-list"), payload)

    assert response.status_code == 201
    assert response.data["name"] == TEST_NAME
    assert response.data["slug"] == TEST_NAME.lower() + TEST_SIZE
    assert response.data["size"] == TEST_SIZE
    assert response.data["cost"] == TEST_COST
    assert response.data["category"] == merch_categories[2].pk


@pytest.mark.django_db
def test_create_merch_fail_if_not_authenticated(client, merch_categories):
    payload = {
        "name": TEST_NAME,
        "size": TEST_SIZE,
        "cost": TEST_COST,
        "category": merch_categories[2].pk,
    }
    response = client.post(reverse("api:merch-list"), payload)

    assert response.status_code == 401
    assert response.data["type"] == "client_error"
    assert response.data["errors"][0]["code"] == "not_authenticated"


@pytest.mark.django_db
def test_create_merch_fail_no_name(auth_client, merch_categories):
    payload = {
        "size": TEST_SIZE,
        "cost": TEST_COST,
        "category": merch_categories[2].pk,
    }
    response = auth_client.post(reverse("api:merch-list"), payload)

    assert response.status_code == 400
    assert response.data["type"] == "validation_error"
    assert response.data["errors"][0]["code"] == "required"
    assert response.data["errors"][0]["attr"] == "name"


@pytest.mark.django_db
def test_create_merch_fail_no_cost(auth_client, merch_categories):
    payload = {
        "name": TEST_NAME,
        "size": TEST_SIZE,
        "category": merch_categories[2].pk,
    }
    response = auth_client.post(reverse("api:merch-list"), payload)

    assert response.status_code == 400
    assert response.data["type"] == "validation_error"
    assert response.data["errors"][0]["code"] == "required"
    assert response.data["errors"][0]["attr"] == "cost"


@pytest.mark.django_db
def test_create_merch_fail_negative_cost(auth_client, merch_categories):
    payload = {
        "name": TEST_NAME,
        "size": TEST_SIZE,
        "cost": -TEST_COST,
        "category": merch_categories[2].pk,
    }
    response = auth_client.post(reverse("api:merch-list"), payload)

    assert response.status_code == 400
    assert response.data["type"] == "validation_error"
    assert response.data["errors"][0]["code"] == "min_value"
    assert response.data["errors"][0]["attr"] == "cost"


@pytest.mark.django_db
def test_create_merch_fail_no_category(auth_client):
    payload = {
        "name": TEST_NAME,
        "size": TEST_SIZE,
        "cost": TEST_COST,
    }
    response = auth_client.post(reverse("api:merch-list"), payload)

    assert response.status_code == 400
    assert response.data["type"] == "validation_error"
    assert response.data["errors"][0]["code"] == "required"
    assert response.data["errors"][0]["attr"] == "category"


@pytest.mark.django_db
def test_edit_merch_name(auth_client, merch):
    old_value = merch[0].name
    payload = {"name": TEST_NAME}
    response = auth_client.patch(
        reverse("api:merch-detail", kwargs={"pk": merch[0].pk}), payload
    )

    assert response.status_code == 200
    assert response.data["name"] == TEST_NAME
    assert merch[0].name != old_value
    assert response.data["id"] == merch[0].pk


@pytest.mark.django_db
def test_edit_merch_size(auth_client, merch):
    old_value = merch[0].size
    payload = {"size": TEST_SIZE}
    response = auth_client.patch(
        reverse("api:merch-detail", kwargs={"pk": merch[0].pk}), payload
    )

    assert response.status_code == 200
    assert response.data["size"] == TEST_SIZE
    assert merch[0].size != old_value
    assert response.data["id"] == merch[0].pk


@pytest.mark.django_db
def test_edit_merch_slug(auth_client, merch):
    old_value = merch[0].slug
    payload = {"slug": TEST_SLUG}
    response = auth_client.patch(
        reverse("api:merch-detail", kwargs={"pk": merch[0].pk}), payload
    )

    assert response.status_code == 200
    assert response.data["slug"] == TEST_SLUG
    assert merch[0].slug != old_value
    assert response.data["id"] == merch[0].pk


@pytest.mark.django_db
def test_edit_merch_cost(auth_client, merch):
    old_value = merch[0].cost
    payload = {"cost": TEST_COST}
    response = auth_client.patch(
        reverse("api:merch-detail", kwargs={"pk": merch[0].pk}), payload
    )

    assert response.status_code == 200
    assert response.data["cost"] == TEST_COST
    assert merch[0].cost != old_value
    assert response.data["id"] == merch[0].pk


@pytest.mark.django_db
def test_edit_merch_category(auth_client, merch, merch_categories):
    old_value = merch[0].category.pk
    payload = {"category": merch_categories[0].pk}
    response = auth_client.patch(
        reverse("api:merch-detail", kwargs={"pk": merch[0].pk}), payload
    )

    assert response.status_code == 200
    assert response.data["category"] == merch_categories[0].pk
    assert merch[0].category != old_value
    assert response.data["id"] == merch[0].pk


@pytest.mark.django_db
def test_delete_merch(auth_client, merch):
    response = auth_client.delete(
        reverse("api:merch-detail", kwargs={"pk": merch[0].pk})
    )

    assert response.status_code == 200
    assert response.data["message"] == MESSAGE_ON_DELETE
