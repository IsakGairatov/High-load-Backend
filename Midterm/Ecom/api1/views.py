from itertools import product

import django_filters
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import viewsets, generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .tasks import *

from .models import *
from .serializers import *


@permission_classes([AllowAny])
# Create your views here.
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']


    @method_decorator(cache_page(60 * 5))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@permission_classes([AllowAny])
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.prefetch_related('product_set')
    serializer_class = CategorySerializer



@permission_classes([IsAuthenticated])
@api_view(["GET", "POST", "DELETE"])
def MyAdress(request):
    if request.method == 'GET':
        items = Adress.objects.filter(user=request.user)
        serializer = AdressSerializer(items, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = request.data
        data2 = {'user': request.user.id, 'country': data['country'], 'city': data['city'], 'street': data['street'], 'house': data['house'], 'flat': data['flat']}

        serializer = AdressSerializer(data=data2)
        print(data)
        if serializer.is_valid():

            serializer.save()
            return JsonResponse(serializer.data, status=201)


        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        item = Adress.objects.filter(user=request.user, id=request.data['id'])
        item.delete()
        return HttpResponse(status=204)

# BusketItems

@cache_page(60 * 5)
@vary_on_cookie
@permission_classes([IsAuthenticated])
@api_view(["GET", "POST", "DELETE"])
def MyBusketItems(request):
    if request.method == 'GET':
        items = BusketItems.objects.filter(buyer=request.user).prefetch_related('product')
        serializer = BusketItemsSerializer(items, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = request.data
        data2 = {'buyer': request.user.id, 'product': data['product']}

        serializer = BusketItemsSerializer(data=data2)
        print(data)
        if serializer.is_valid():

            serializer.save()
            return JsonResponse(serializer.data, status=201)


        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        item = BusketItems.objects.filter(buyer=request.user, id=request.data['id'])
        item.delete()
        return HttpResponse(status=204)

@permission_classes([IsAuthenticated])
@api_view(["POST"])
def BuyAllBusket(request):
    data = request.data
    adress = Adress.objects.get(id=data['adress_id'])
    cardnums = data['cardnums']

    if request.method == 'POST':
        MyBusketItems = BusketItems.objects.filter(buyer=request.user)
        for item in MyBusketItems:
            try:
                BuyItem.delay(request.user.id, item.product.id, adress.id, cardnums)
                item.delete()
            except:
                print("Error while buying product" + str(item.id))
        return HttpResponse(status=204)

@permission_classes([IsAuthenticated])
@api_view(["POST"])
def Buy(request):
    data = request.data
    adress_id = data['adress_id']
    cardnums = data['cardnums']

    pr = Product.objects.get(id=data['product_id'])


    BuyItem.delay(request.user.id, pr.id, adress_id, cardnums)
    return HttpResponse(status=204)


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def MyPurchases(request):
    if request.method == 'GET':
        items = Purchase.objects.filter(buyer=request.user)
        serializer = PurchaseSerializer(items, many=True)
        return JsonResponse(serializer.data, safe=False)


#Login User
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#Register User
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@permission_classes([IsAuthenticated])
@api_view(["GET"])
def Me(request):
    if request.method == 'GET':
        return HttpResponse(request.user)






