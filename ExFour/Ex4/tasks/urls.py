from django.urls import path
from .views import EmailAPIView, FileUploadAPIView

urlpatterns = [
    path('api/send-email/', EmailAPIView.as_view(), name='send_email'),
    path('upload/', FileUploadAPIView.as_view(), name='file-upload'),
]