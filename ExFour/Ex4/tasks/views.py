from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Email
from .serializers import EmailSerializer
from .tasks import send_email_task
from rest_framework import permissions

class EmailAPIView(APIView):
    permission_classes = permissions.IsAdminUser
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.save()
            send_email_task.delay(email.id)
            return Response({"message": "Email queued successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UploadedFile
from .tasks import process_file_task


class FileUploadAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file_obj = request.data['file']
        uploaded_file = UploadedFile.objects.create(file=file_obj)
        process_file_task.delay(uploaded_file.id)
        return Response({"message": "File upload queued successfully!"})

