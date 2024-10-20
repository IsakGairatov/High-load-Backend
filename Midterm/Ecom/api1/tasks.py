from celery import shared_task
from django.contrib.auth.models import User

from .models import Product, Purchase, Adress

@shared_task
def BuyItem(user_id, pr_id, adress_id, card):
    pr = Product.objects.get(id=pr_id)
    adress = Adress.objects.get(id=adress_id)
    user = User.objects.get(id=user_id)

    if pr.amount > 0:
        Purchase.objects.create(
            product=pr,
            buyer=user,
            adress=adress,
            cardLast4nums=card,
            )
        pr.amount = pr.amount - 1
        pr.save()