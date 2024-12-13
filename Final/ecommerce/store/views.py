import logging

from django.db import transaction
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .tasks import process_payment_task

from .models import *
from .serializers import *


#Logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# JWT Login


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#Register User
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# Model views

#@cache_page(60 * 1)
#@vary_on_cookie
@api_view(['GET'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, id):
    if request.method == 'GET':
        product = Product.objects.prefetch_related('reviews').get(id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

@api_view(['GET'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.prefetch_related('products').all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

@cache_page(60 * 1)
@vary_on_cookie
@api_view(['GET'])
def category_detail(request, id):
    if request.method == 'GET':
        products = Product.objects.filter(category__id=id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def order_create(request):
    if request.method == 'POST':
        order_items_data = request.data.get('order_items')

        def order_price(id, quantity):
            return Product.objects.get(id=id).price * quantity

        total_amount = sum(order_price(item['product_id'],item['quantity']) for item in order_items_data)

        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            order_status='Pending'
        )

        for item_data in order_items_data:
            product = Product.objects.get(id=item_data['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=product.price
            )

        return Response({"message": "Order placed successfully!"}, status=status.HTTP_201_CREATED)



@cache_page(60 * 1)
@vary_on_cookie
@api_view(['GET'])
def shopping_cart(request):
    if request.method == 'GET':
        cart, created = ShoppingCart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.select_related('product').filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response({"cart_items": serializer.data})


@api_view(['POST'])
def add_item_to_cart(request):
    if request.method == 'POST':
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        product = Product.objects.get(id=product_id)
        cart, created = ShoppingCart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, quantity=quantity)
        cart_item.save()

        return Response({"message": "Item added to cart"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def order_cart(request):
    user = request.user

    try:
        # Retrieve the user's shopping cart
        cart = ShoppingCart.objects.get(user=user)

        # If there are no items in the cart, return an error
        if not cart.cart_items.exists():
            return Response({"message": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new order
        with transaction.atomic():
            # Calculate the total amount for the order
            total_amount = 0
            for cart_item in cart.cart_items.all():
                product = cart_item.product
                quantity = cart_item.quantity
                if product.stock_quantity < quantity:
                    return Response({"message": f"Not enough stock for product {product.name}."}, status=status.HTTP_400_BAD_REQUEST)

                total_amount += product.price * quantity

            # Create the order
            order = Order.objects.create(
                user=user,
                total_amount=total_amount,
                order_status='pending',  # You can modify this as needed
            )

            # Create order items and decrease the stock of each product
            for cart_item in cart.cart_items.all():
                product = cart_item.product
                quantity = cart_item.quantity
                price = product.price

                # Create order items
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )

            # Clear the cart after the order is placed
            cart.cart_items.all().delete()

            return Response({"message": "Order placed successfully!"}, status=status.HTTP_201_CREATED)

    except ShoppingCart.DoesNotExist:
        return Response({"message": "Shopping cart not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@cache_page(60 * 1)
@vary_on_cookie
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_wishlist(request):
    if request.method == 'GET':
        # Get the user's wishlist
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist_items = WishlistItem.objects.select_related('product').filter(wishlist=wishlist)

        # Serialize the wishlist items
        serializer = WishlistItemSerializer(wishlist_items, many=True)

        # Return the wishlist items
        return Response({"wishlist_items": serializer.data})

@api_view(['POST'])
def add_to_wishlist(request):
    if request.method == 'POST':
        product_id = request.data.get('product_id')

        product = Product.objects.get(id=product_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)

        wishlist_item, created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)

        return Response({"message": "Product added to wishlist"}, status=status.HTTP_200_OK)

@cache_page(60 * 1)
@vary_on_cookie
@api_view(['GET'])
def view_product_reviews(request, product_id):
    if request.method == 'GET':
        # Get all reviews for this product
        reviews = Review.objects.filter(product__id=product_id)

        # Serialize the reviews
        serializer = ReviewSerializer(reviews, many=True)

        return Response({"reviews": serializer.data})


@api_view(['POST'])
def create_review(request):
    if request.method == 'POST':
        product_id = request.data.get('product_id')
        rating = request.data.get('rating')
        comment = request.data.get('comment')

        product = Product.objects.get(id=product_id)

        review = Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )

        return Response({"message": "Review added successfully"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_payments(request):
    if request.method == 'GET':
        # Get all payments related to the user's orders
        payments = Payment.objects.filter(order__user=request.user)

        # Serialize the payments data
        serializer = PaymentSerializer(payments, many=True)

        return Response({"payments": serializer.data})


@api_view(['POST'])
def process_payment(request):
    if request.method == 'POST':
        order_id = request.data.get('order_id')
        amount = request.data.get('amount')
        payment_method = request.data.get('payment_method')

        # Call the Celery task to process payment asynchronously
        process_payment_task.delay(order_id, amount, payment_method)

        return Response({"message": "Payment is being processed."}, status=status.HTTP_202_ACCEPTED)


