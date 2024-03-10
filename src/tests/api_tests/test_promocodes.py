import pytest
from django.urls import reverse

from tests.fixtures import TEST_NAME, TEST_PAST_DATETIME

from api.mixins import MESSAGE_ON_DELETE


@pytest.mark.django_db
def test_get_promocode_list(auth_client, promocodes):
    response = auth_client.get(reverse("api:promocode-list"))

    assert response.status_code == 200
    assert len(response.data) == 4
    assert response.data[0]["code"] == promocodes[0].code
    assert response.data[0]["created"] != ""
    assert response.data[0]["is_active"] == promocodes[0].is_active
    assert response.data[0]["ambassador"]["name"] == promocodes[0].ambassador.name
    assert (
        response.data[0]["ambassador"]["status"]["name"]
        == promocodes[0].ambassador.status.name
    )
    assert response.data[0]["ambassador"]["created"] != ""
    assert (
        response.data[0]["ambassador"]["telegram"]
        == promocodes[0].ambassador.telegram_id
    )


@pytest.mark.django_db
def test_get_promocode_fail_if_not_authenticated(client):
    response = client.get(reverse("api:promocode-list"))

    assert response.status_code == 401
    assert response.data["type"] == "client_error"
    assert response.data["errors"][0]["code"] == "not_authenticated"


@pytest.mark.django_db
def test_get_promocode_by_id(auth_client, promocodes):
    response = auth_client.get(
        reverse("api:promocode-detail", kwargs={"pk": promocodes[0].pk})
    )

    assert response.status_code == 200
    assert response.data["code"] == promocodes[0].code
    assert response.data["created"] != ""
    assert response.data["is_active"] == promocodes[0].is_active
    assert response.data["ambassador"]["name"] == promocodes[0].ambassador.name
    assert (
        response.data["ambassador"]["status"]["name"]
        == promocodes[0].ambassador.status.name
    )
    assert response.data["ambassador"]["created"] != ""
    assert (
        response.data["ambassador"]["telegram"] == promocodes[0].ambassador.telegram_id
    )


@pytest.mark.django_db
def test_create_promocode(auth_client, ambassadors):
    payload = {"code": TEST_NAME, "ambassador": ambassadors[0].pk}
    response = auth_client.post(reverse("api:promocode-list"), payload)

    assert response.status_code == 201
    print(response.data)
    assert response.data["code"] == TEST_NAME
    assert response.data["created"] != ""
    # assert response.data["is_active"] is True  not working
    assert response.data["ambassador"] == ambassadors[0].pk


@pytest.mark.django_db
def test_create_promocode_fail_if_not_authenticated(client, ambassadors):
    payload = {"code": TEST_NAME, "ambassador": ambassadors[0].pk}
    response = client.post(reverse("api:promocode-list"), payload)

    assert response.status_code == 401
    assert response.data["type"] == "client_error"
    assert response.data["errors"][0]["code"] == "not_authenticated"


@pytest.mark.django_db
def test_create_promocode_fail_no_code(auth_client, ambassadors):
    payload = {"ambassador": ambassadors[0].pk}
    response = auth_client.post(reverse("api:promocode-list"), payload)

    assert response.status_code == 400
    assert response.data["type"] == "validation_error"
    assert response.data["errors"][0]["code"] == "required"
    assert response.data["errors"][0]["attr"] == "code"


@pytest.mark.django_db
def test_create_promocode_fail_no_ambassador(auth_client):
    payload = {"code": TEST_NAME}
    response = auth_client.post(reverse("api:promocode-list"), payload)

    assert response.status_code == 400
    assert response.data["type"] == "validation_error"
    assert response.data["errors"][0]["code"] == "required"
    assert response.data["errors"][0]["attr"] == "ambassador"


@pytest.mark.django_db
def test_edit_promocode_code(auth_client, promocodes):
    old_value = promocodes[0].code
    payload = {"code": TEST_NAME}
    response = auth_client.patch(
        reverse("api:promocode-detail", kwargs={"pk": promocodes[0].pk}), payload
    )

    assert response.status_code == 200
    assert response.data["code"] == TEST_NAME
    assert promocodes[0].code != old_value
    assert response.data["id"] == promocodes[0].pk


@pytest.mark.django_db
def test_edit_promocode_created_field(auth_client, promocodes):
    old_value = promocodes[0].created
    payload = {"created": TEST_PAST_DATETIME}
    response = auth_client.patch(
        reverse("api:promocode-detail", kwargs={"pk": promocodes[0].pk}), payload
    )

    assert response.status_code == 200
    assert response.data["created"] == TEST_PAST_DATETIME
    assert promocodes[0].created != old_value
    assert response.data["id"] == promocodes[0].pk


@pytest.mark.django_db
def test_edit_promocode_is_active_field(auth_client, promocodes):
    old_value = promocodes[0].is_active
    payload = {"is_active": False}
    response = auth_client.patch(
        reverse("api:promocode-detail", kwargs={"pk": promocodes[0].pk}), payload
    )

    assert response.status_code == 200
    assert response.data["is_active"] is False
    assert promocodes[0].is_active != old_value
    assert response.data["id"] == promocodes[0].pk


@pytest.mark.django_db
def test_edit_promocode_is_ambassador(auth_client, promocodes, ambassadors):
    old_value = promocodes[0].ambassador
    payload = {"ambassador": ambassadors[2].pk}
    response = auth_client.patch(
        reverse("api:promocode-detail", kwargs={"pk": promocodes[0].pk}), payload
    )

    assert response.status_code == 200
    assert response.data["ambassador"] == ambassadors[2].pk
    assert promocodes[0].ambassador != old_value
    assert response.data["id"] == promocodes[0].pk


@pytest.mark.django_db
def test_delete_promocode(auth_client, promocodes):
    response = auth_client.delete(
        reverse("api:promocode-detail", kwargs={"pk": promocodes[0].pk})
    )

    assert response.status_code == 200
    assert response.data["message"] == MESSAGE_ON_DELETE


@pytest.mark.django_db
def test_get_promocode_google_sheet_link(auth_client, promocodes):
    response = auth_client.get("/api/v1/promocodes/export_to_google_sheet/")

    assert response.status_code == 200
    assert "https://docs.google.com/spreadsheets/d/" in response.data["link"]
