# tests/test_order_processing.py

from rest_framework.test import APIClient
from rest_framework import status
from ..models import Product, Order, User
import pytest


@pytest.mark.django_db
def test_create_order():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='password123')
    client.force_authenticate(user=user)

    # Create a product to add to the order
    product = Product.objects.create(name='Test Product', price=100, stock_quantity=10)

    order_data = {
        "order_items": [
            {
                "product_id": product.id,
                "quantity": 2
            }
        ]
    }

    response = client.post('/api/orders/create/', order_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Order.objects.count() == 1
    assert Order.objects.first().total_amount == 200  # price * quantity
