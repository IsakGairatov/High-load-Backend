from django.db.models.fields import return_None
from django.urls import path
from django.views.generic import RedirectView

from .views import *

urlpatterns = [
    path('', RedirectView.as_view(url='posts/')),
    path('posts/', showPosts, name='Posts'),
    path('posts/tag/<int:tag_id>/', showTagPosts, name='TagPosts'),
    path('posts/<int:id>/', showPost, name='postpage'),
    path('posts/makepost/', makePost, name='makepost'),
    path('posts/<int:id>/editpost/', editPost, name='editPost'),
    path('deltag/<int:post>/<int:tag>/', deltag, name='delTag'),
    path('posts/<int:id>/delete/', delPost, name='delPost'),



    path('me/', Profile, name='Profile'),
    path('me/edit/', ProfileEdit, name='profileEdit'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('registration/', RegisterUser.as_view(), name='registration'),



]