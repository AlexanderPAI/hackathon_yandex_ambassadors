import pytest
from django.urls import reverse

from tests.fixtures import TEST_NUMBER, TEST_PAST_DATETIME

from api.mixins import MESSAGE_ON_DELETE


@pytest.mark.django_db
def test_get_merch_applications_list(
    auth_client, merch_applications, ambassadors, merch
):
    response = auth_client.get(reverse("api:merchapplication-list"))

    assert response.status_code == 200
    assert len(response.data) == 3
    assert (
        response.data[0]["application_number"]
        == merch_applications[0].application_number
    )
    assert (
        response.data[0]["ambassador"]["name"] == merch_applications[0].ambassador.name
    )
    assert (
        response.data[0]["tutor"]["full_name"]
        == merch_applications[0].tutor.get_full_name()
    )
    assert (
        response.data[0]["merch"][0]["name"]
        == merch_applications[0].merch.all()[0].name
    )


@pytest.mark.django_db
def test_get_merch_applications_fail_if_not_authenticated(client):
    response = client.get(reverse("api:merchapplication-list"))

    assert response.status_code == 401
    assert response.data["type"] == "client_error"
    assert response.data["errors"][0]["code"] == "not_authenticated"


@pytest.mark.django_db
def test_get_merch_applications_by_id(auth_client, merch_applications):
    response = auth_client.get(
        reverse("api:merchapplication-detail", kwargs={"pk": merch_applications[0].pk})
    )

    assert response.status_code == 200
    assert (
        response.data["application_number"] == merch_applications[0].application_number
    )
    assert response.data["ambassador"]["name"] == merch_applications[0].ambassador.name
    assert (
        response.data["tutor"]["full_name"]
        == merch_applications[0].tutor.get_full_name()
    )
    assert (
        response.data["merch"][0]["name"] == merch_applications[0].merch.all()[0].name
    )


@pytest.mark.django_db
def test_create_merch_applications(auth_client, ambassadors, user, merch):
    payload = {
        "ambassador": ambassadors[0].pk,
        "merch": [{"id": merch[0].pk, "quantity": 10}],
    }
    response = auth_client.post(
        reverse("api:merchapplication-list"), payload, format="json"
    )

    assert response.status_code == 201
    assert "2024" in response.data["application_number"]
    assert response.data["ambassador"] == ambassadors[0].pk
    assert response.data["tutor"] == user.pk
    assert "2024" in response.data["created"]
    assert response.data["merch"][0]["id"] == merch[0].pk
    assert response.data["merch"][0]["name"] == merch[0].name
    assert response.data["merch"][0]["category"] == merch[0].category.name
    assert response.data["merch"][0]["slug"] == merch[0].slug
    assert response.data["merch"][0]["size"] == merch[0].size
    assert response.data["merch"][0]["cost"] == merch[0].cost
    assert response.data["merch"][0]["quantity"] == 10


@pytest.mark.django_db
def test_create_merch_applications_if_not_authenticated(
    client, ambassadors, user, merch
):
    payload = {
        "ambassador": ambassadors[0].pk,
        "merch": [{"id": merch[0].pk, "quantity": 10}],
    }
    response = client.post(reverse("api:merchapplication-list"), payload, format="json")

    assert response.status_code == 401
    assert response.data["type"] == "client_error"
    assert response.data["errors"][0]["code"] == "not_authenticated"


@pytest.mark.django_db
def test_create_merch_applications_fail_if_no_ambassador(auth_client, merch):
    payload = {"merch": [{"id": merch[0].pk, "quantity": 10}]}
    response = auth_client.post(
        reverse("api:merchapplication-list"), payload, format="json"
    )

    assert response.status_code == 400
    assert response.data["type"] == "validation_error"
    assert response.data["errors"][0]["code"] == "required"
    assert response.data["errors"][0]["attr"] == "ambassador"


@pytest.mark.django_db
def test_create_merch_applications_if_no_merch(auth_client, ambassadors):
    payload = {"ambassador": ambassadors[0].pk}
    response = auth_client.post(
        reverse("api:merchapplication-list"), payload, format="json"
    )

    assert response.status_code == 400
    assert response.data["type"] == "validation_error"
    assert response.data["errors"][0]["code"] == "required"
    assert response.data["errors"][0]["attr"] == "merch"


@pytest.mark.django_db
def test_edit_merch_applications_application_number(auth_client, merch_applications):
    old_value = merch_applications[0].application_number
    payload = {"application_number": TEST_NUMBER}
    response = auth_client.patch(
        reverse("api:merchapplication-detail", kwargs={"pk": merch_applications[0].pk}),
        payload,
    )

    assert response.status_code == 200
    assert response.data["application_number"] == TEST_NUMBER
    assert merch_applications[0].application_number != old_value
    assert response.data["id"] == merch_applications[0].pk


@pytest.mark.django_db
def test_edit_merch_applications_ambassador(
    auth_client, merch_applications, ambassadors
):
    old_value = merch_applications[0].ambassador.pk
    payload = {"ambassador": ambassadors[1].pk}
    response = auth_client.patch(
        reverse("api:merchapplication-detail", kwargs={"pk": merch_applications[0].pk}),
        payload,
    )

    assert response.status_code == 200
    assert response.data["ambassador"] == ambassadors[1].pk
    assert merch_applications[0].ambassador != old_value
    assert response.data["id"] == merch_applications[0].pk


@pytest.mark.django_db
def test_edit_merch_applications_created_field(auth_client, merch_applications):
    old_value = merch_applications[0].created
    payload = {"created": TEST_PAST_DATETIME}
    response = auth_client.patch(
        reverse("api:merchapplication-detail", kwargs={"pk": merch_applications[0].pk}),
        payload,
    )

    assert response.status_code == 200
    assert response.data["created"] == TEST_PAST_DATETIME
    assert merch_applications[0].created != old_value
    assert response.data["id"] == merch_applications[0].pk


@pytest.mark.django_db
def test_edit_merch_applications_merch(auth_client, merch_applications, merch):
    old_merch = merch_applications[0].merch_in_applications.first().merch.name
    old_quantity = merch_applications[0].merch_in_applications.first().quantity
    payload = {"merch": [{"id": merch[5].pk, "quantity": 3}]}
    response = auth_client.patch(
        reverse("api:merchapplication-detail", kwargs={"pk": merch_applications[0].pk}),
        payload,
        format="json",
    )

    assert response.status_code == 200
    assert response.data["merch"][0]["id"] == merch[5].pk
    assert response.data["merch"][0]["quantity"] == 3
    assert merch_applications[0].merch_in_applications.first().merch.name != old_merch
    assert merch_applications[0].merch_in_applications.first().quantity != old_quantity
    assert response.data["id"] == merch_applications[0].pk


@pytest.mark.django_db
def test_delete_merch_applications(auth_client, merch_applications):
    response = auth_client.delete(
        reverse("api:merchapplication-detail", kwargs={"pk": merch_applications[0].pk})
    )

    assert response.status_code == 200
    assert response.data["message"] == MESSAGE_ON_DELETE


@pytest.mark.django_db
def test_delete_merch_budget_info(auth_client, merch, merch_applications):
    year_total = merch[0].cost * 2 + merch[1].cost * 4 + merch[2].cost * 10
    response = auth_client.get("/api/v1/send_merch/budget_info/?year=2024")

    assert response.status_code == 200
    assert response.data["year"] == 2024
    assert response.data["year_total"] == year_total
