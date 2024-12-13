from celery import shared_task
from .models import Order, Payment, OrderItem, Product
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_payment_task(order_id, amount, payment_method):
    try:
        # Retrieve the order by ID
        order = Order.objects.get(id=order_id)

        # Check if the payment amount matches the total amount
        if amount != order.total_amount:
            logger.error(f"Payment amount mismatch for order {order_id}.")
            return "Payment amount does not match order total."

        # Assume payment is successful and create the payment record
        payment = Payment.objects.create(
            order=order,
            payment_method=payment_method,
            amount=amount,
            status='Completed'
        )

        # Mark the order as paid
        order.order_status = 'Paid'
        order.save()

        # Decrease the stock for each product in the order
        for order_item in OrderItem.objects.filter(order=order):
            product = order_item.product
            product.stock_quantity -= order_item.quantity
            product.save()

        return "Payment successful and stock updated."
    except Order.DoesNotExist:
        logger.error(f"Order with id {order_id} not found.")
        return "Order not found."
    except Exception as e:
        logger.error(f"Error processing payment for order {order_id}: {str(e)}")
        return f"Error processing payment: {str(e)}"