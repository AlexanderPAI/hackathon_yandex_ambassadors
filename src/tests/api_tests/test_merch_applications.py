import pytest
from django.urls import reverse


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
