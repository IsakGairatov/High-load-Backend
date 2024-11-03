from django.urls import path
from .views import key_value_store

urlpatterns = [
    path('store/<str:key>/', key_value_store),
]