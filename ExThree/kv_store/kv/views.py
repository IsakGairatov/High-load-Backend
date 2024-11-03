from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import KeyValue
from .serializers import KeyValueSerializer

import logging
logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
def key_value_store(request, key=None):
    if request.method == 'POST':
        val = request.data.get('value')
        kv, created = KeyValue.objects.update_or_create(key=key, defaults={'value': val})
        serializer = KeyValueSerializer(kv)

        logger.debug("Key Value Get request")
        return Response(serializer.data)

    elif request.method == 'GET' and key is not None:
        try:
            kv = KeyValue.objects.get(key=key)
            serializer = KeyValueSerializer(kv)
            return Response(serializer.data)
        except KeyValue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)





