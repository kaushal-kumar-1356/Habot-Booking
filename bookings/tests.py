import pytest
from rest_framework.test import APIClient

from bookings.models import Parent, LSA_Profile, Booking_Request



@pytest.mark.django_db
def test_parent_can_be_created():

    parent = Parent.objects.create(
        name="Test Parent",
        email="testparent@example.com",
        phone="9876543210"
    )

    assert parent.name == "Test Parent"
    assert parent.email == "testparent@example.com"




@pytest.mark.django_db
def test_booking_can_be_created():

    parent = Parent.objects.create(
        name="Rahul",
        email="rahul@test.com",
        phone="9876543210"
    )

    lsa = LSA_Profile.objects.create(
        name="John",
        email="john@test.com",
        skills="Maths, English"
    )

    client = APIClient()

    response = client.post(
        "/api/v1/bookings/",
        {
            "parent": parent.id,
            "lsa": lsa.id,
            "start_time": "2026-08-13T10:00:00Z",
            "end_time": "2026-08-13T11:00:00Z"
        },
        format="json"
    )

    assert response.status_code == 201
    assert Booking_Request.objects.count() == 1



@pytest.mark.django_db
def test_double_booking_is_rejected():

    parent1 = Parent.objects.create(
        name="Rahul",
        email="rahul1@test.com",
        phone="9876543210"
    )

    parent2 = Parent.objects.create(
        name="Amit",
        email="amit@test.com",
        phone="9876543211"
    )

    lsa = LSA_Profile.objects.create(
        name="John",
        email="john1@test.com",
        skills="Maths"
    )

    client = APIClient()

    first_response = client.post(
        "/api/v1/bookings/",
        {
            "parent": parent1.id,
            "lsa": lsa.id,
            "start_time": "2026-08-13T10:00:00Z",
            "end_time": "2026-08-13T11:00:00Z"
        },
        format="json"
    )

    second_response = client.post(
        "/api/v1/bookings/",
        {
            "parent": parent2.id,
            "lsa": lsa.id,
            "start_time": "2026-08-13T10:30:00Z",
            "end_time": "2026-08-13T11:30:00Z"
        },
        format="json"
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409




@pytest.mark.django_db
def test_end_time_must_be_after_start_time():

    parent = Parent.objects.create(
        name="Test Parent",
        email="time@test.com",
        phone="9876543212"
    )

    lsa = LSA_Profile.objects.create(
        name="Test LSA",
        email="time.lsa@test.com",
        skills="English"
    )

    client = APIClient()

    response = client.post(
        "/api/v1/bookings/",
        {
            "parent": parent.id,
            "lsa": lsa.id,
            "start_time": "2026-08-13T12:00:00Z",
            "end_time": "2026-08-13T11:00:00Z"
        },
        format="json"
    )

    assert response.status_code == 400




@pytest.mark.django_db
def test_lsa_search_by_skill():

    LSA_Profile.objects.create(
        name="John Smith",
        email="john.search@test.com",
        skills="Maths, English"
    )

    LSA_Profile.objects.create(
        name="Priya Sharma",
        email="priya.search@test.com",
        skills="Science, Maths"
    )

    LSA_Profile.objects.create(
        name="Amit Kumar",
        email="amit.search@test.com",
        skills="English, Computer"
    )

    client = APIClient()

    response = client.get(
        "/api/v1/lsas/search/?skill=maths"
    )

    assert response.status_code == 200
    assert len(response.data) == 2

    names = [lsa["name"] for lsa in response.data]

    assert "John Smith" in names
    assert "Priya Sharma" in names
    assert "Amit Kumar" not in names




@pytest.mark.django_db
def test_payment_can_be_created():

    parent = Parent.objects.create(
        name="Payment Parent",
        email="payment.parent@test.com",
        phone="9876543213"
    )

    lsa = LSA_Profile.objects.create(
        name="Payment LSA",
        email="payment.lsa@test.com",
        skills="Maths"
    )

    client = APIClient()

    booking_response = client.post(
        "/api/v1/bookings/",
        {
            "parent": parent.id,
            "lsa": lsa.id,
            "start_time": "2026-08-14T10:00:00Z",
            "end_time": "2026-08-14T11:00:00Z"
        },
        format="json"
    )

    assert booking_response.status_code == 201

    booking_id = booking_response.data["id"]

    payment_response = client.post(
        "/api/v1/payments/",
        {
            "booking": booking_id,
            "amount": "500.00"
        },
        format="json"
    )

    assert payment_response.status_code == 201
    assert payment_response.data["status"] == "SUCCESS"
    assert payment_response.data["transaction_id"] is not None




@pytest.mark.django_db
def test_payment_webhook_confirms_booking():

    parent = Parent.objects.create(
        name="Webhook Parent",
        email="webhook.parent@test.com",
        phone="9876543214"
    )

    lsa = LSA_Profile.objects.create(
        name="Webhook LSA",
        email="webhook.lsa@test.com",
        skills="English"
    )

    client = APIClient()

    booking_response = client.post(
        "/api/v1/bookings/",
        {
            "parent": parent.id,
            "lsa": lsa.id,
            "start_time": "2026-08-14T12:00:00Z",
            "end_time": "2026-08-14T13:00:00Z"
        },
        format="json"
    )

    assert booking_response.status_code == 201

    booking_id = booking_response.data["id"]

    webhook_response = client.post(
        "/api/v1/payments/webhook/",
        {
            "booking_id": booking_id,
            "status": "SUCCESS"
        },
        format="json"
    )

    assert webhook_response.status_code == 200

    booking = Booking_Request.objects.get(
        id=booking_id
    )

    assert booking.status == "CONFIRMED"