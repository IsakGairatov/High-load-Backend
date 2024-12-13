from django.urls import path
from django_ratelimit.decorators import ratelimit
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [

    # Jwt authentification
    path('token/', ratelimit(key='ip', rate='5/m')(TokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', ratelimit(key='ip', rate='5/m')(RegisterView.as_view()), name='auth_register'),

    # Product views
    path('products/', product_list, name='product-list'),
    path('products/<int:id>/', product_detail, name='product-detail'),

    # Category views
    path('categories/', category_list, name='category-list'),
    path('categories/<int:id>/', category_detail, name='category-detail'),

    # Order views
    path('orders/', order_list, name='order-list'),  # Will require authentication
    path('orders/create/', order_create, name='order-create'),

    # Shopping Cart views
    path('cart/', shopping_cart, name='shopping-cart'),  # Will require authentication
    path('cart/add/', add_item_to_cart, name='add-to-cart'),
    path('order/cart/', order_cart, name='order_cart'),

    # Wishlist views
    path('wishlist/', view_wishlist, name='view-wishlist'),  # Requires authentication
    path('wishlist/add/', add_to_wishlist, name='add-to-wishlist'),  # Will require authentication

    # Review views
    path('reviews/product/<int:product_id>/', view_product_reviews, name='view-product-reviews'),
    path('reviews/create/', create_review, name='create-review'),  # Will require authentication

    # Payment views
    path('payments/', view_payments, name='view-payments'),  # Requires authentication
    path('payment/', process_payment, name='process-payment'),  # Will require authentication
]