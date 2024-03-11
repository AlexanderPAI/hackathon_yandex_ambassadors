import pytest


@pytest.mark.django_db
def test_get_ambassador_list(auth_client, ambassadors):
    response = auth_client.get("/api/v1/ambassadors/")
    assert response.status_code == 200
    assert len(response.data) == 3
    assert response.data[0]["name"] == ambassadors[2].name
    assert response.data[0]["created"] != ""
    assert response.data[0]["gender"] == ambassadors[2].gender
    assert response.data[0]["clothing_size"] == ambassadors[2].clothing_size
    assert response.data[0]["shoe_size"] == ambassadors[2].shoe_size
    assert response.data[0]["education"] == ambassadors[2].education
    assert response.data[0]["job"] == ambassadors[2].job
    assert response.data[0]["email"] == ambassadors[2].email
    assert response.data[0]["phone_number"] == ambassadors[2].phone_number
    assert response.data[0]["telegram_id"] == ambassadors[2].telegram_id
    assert response.data[0]["whatsapp"] is None
    assert len(response.data[0]["activity"]) == 2
    assert response.data[0]["blog_link"] is None
    assert response.data[0]["onboarding_status"] is False
    assert response.data[0]["purpose"]["name"] == ambassadors[2].purpose.name
    assert response.data[0]["about_me"] is None
    assert response.data[0]["tutor"] is None
    assert response.data[0]["status"]["name"] == ambassadors[2].status.name
    assert response.data[0]["program"]["name"] == ambassadors[2].program.name
    assert response.data[0]["address"]["street"] == ambassadors[2].address.street
    assert response.data[0]["promocodes"] == []
