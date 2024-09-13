from django.urls import path

from .views import *

urlpatterns = [
    path('posts/', showPosts, name='Posts'),
    path('posts/<int:id>/', showPost, name='postpage'),
    path('posts/makepost/', makePost, name='makepost'),

    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('registration/', RegisterUser.as_view(), name='registration'),

    path('posts/<int:id>/delete/', delPost, name='delPost'),
    path('posts/<int:id>/update/', updatePost, name='updatePost'),
]