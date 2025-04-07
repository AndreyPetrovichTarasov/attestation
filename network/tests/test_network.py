import pytest
from django.urls import reverse
from network.models import NetworkNode, Product
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(
        username="admin", password="adminpass", is_staff=True, is_active=True
    )


@pytest.fixture
def auth_api_client(api_client, staff_user):
    api_client.force_authenticate(user=staff_user)
    return api_client


@pytest.fixture
def node():
    return NetworkNode.objects.create(
        name="Test Node",
        email="test@node.com",
        country="Россия",
        city="Москва",
        street="Тестовая",
        house_number="10",
        debt=100.00,
    )


@pytest.fixture
def product(node):
    return Product.objects.create(
        node=node, name="Ноутбук", model="NB-2024", release_date="2024-01-01"
    )


# ---------- 🧪 WEB: NetworkNode ----------


@pytest.mark.django_db
def test_node_list_view(client, node):
    response = client.get(reverse("network:list"))
    assert response.status_code == 200
    assert node.name in response.content.decode()


@pytest.mark.django_db
def test_node_detail_view(client, node):
    url = reverse("network:detail", args=[node.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert node.city in response.content.decode()


@pytest.mark.django_db
def test_node_create_view(client):
    url = reverse("network:create")
    response = client.post(
        url,
        {
            "name": "New Node",
            "email": "new@example.com",
            "country": "Россия",
            "city": "Сочи",
            "street": "Центральная",
            "house_number": "22",
            "debt": 0,
        },
    )
    assert response.status_code == 302  # redirect after success
    assert NetworkNode.objects.filter(name="New Node").exists()


# ---------- 🧪 WEB: Product ----------


@pytest.mark.django_db
def test_product_create_view(client, node):
    url = reverse("network:product_create", args=[node.pk])
    response = client.post(
        url, {"name": "Телевизор", "model": "TV-2024", "release_date": "2024-03-01"}
    )
    assert response.status_code == 302
    assert Product.objects.filter(name="Телевизор", node=node).exists()


# ---------- 🧪 API: NetworkNode ----------


@pytest.mark.django_db
def test_api_list_nodes(auth_api_client, node):
    response = auth_api_client.get("/api/nodes/")
    assert response.status_code == status.HTTP_200_OK
    assert node.name in str(response.data)


@pytest.mark.django_db
def test_api_create_node(auth_api_client):
    response = auth_api_client.post(
        "/api/nodes/",
        {
            "name": "API Node",
            "email": "api@node.com",
            "country": "Беларусь",
            "city": "Минск",
            "street": "Новая",
            "house_number": "5",
            "debt": "50.00",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert NetworkNode.objects.filter(name="API Node").exists()


@pytest.mark.django_db
def test_api_update_node(auth_api_client, node):
    url = f"/api/nodes/{node.pk}/"
    response = auth_api_client.patch(
        url,
        {"city": "Новосибирск", "debt": "0"},  # должно остаться без изменений (запрет)
    )
    node.refresh_from_db()
    assert response.status_code == 200
    assert node.city == "Новосибирск"
    assert node.debt == 100.00  # задолженность не меняется


@pytest.mark.django_db
def test_api_delete_node(auth_api_client, node):
    url = f"/api/nodes/{node.pk}/"
    response = auth_api_client.delete(url)
    assert response.status_code == 204
    assert not NetworkNode.objects.filter(pk=node.pk).exists()


# ---------- 🧪 API: Permissions ----------


@pytest.mark.django_db
def test_api_forbidden_for_anonymous(api_client):
    response = api_client.get("/api/nodes/")
    assert response.status_code == 403
