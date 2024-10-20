from django.http import HttpResponse
from django.urls import path
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'category', CategoryViewSet)



urlpatterns = router.urls + [

    path('MyBusket/', MyBusketItems),
    path('MyBusket/<int:id>/', MyBusketItems),
    path('MyAdress/', MyAdress),
    path('BuyBusket/', BuyAllBusket),
    path('Buy/', Buy),
    path('mypurchases/', MyPurchases),


    path('me/', Me),


    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]
