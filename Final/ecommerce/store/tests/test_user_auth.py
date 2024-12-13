# tests/test_authentication.py

from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
import pytest


@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    user_data = {
        "username": "testuser",
        "password": "password123",
        "email": "testuser@example.com"
    }
    response = client.post('/api/auth/register/', user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'username' in response.data


@pytest.mark.django_db
def test_user_login():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='password123')
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    response = client.post('/api/auth/login/', login_data)
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
