import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_get_merch_list(auth_client):
    response = auth_client.get(reverse("api:merch-list"))
    assert response.status_code == 200
