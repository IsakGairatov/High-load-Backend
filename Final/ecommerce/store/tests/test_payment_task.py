# tests/test_payment_task.py

from ..tasks import process_payment_task
from django.test import TestCase
from unittest.mock import patch


class PaymentTaskTest(TestCase):

    @patch('myapp.tasks.process_payment_task.delay')
    def test_process_payment_task(self, mock_process_payment):
        # Mock the task call and verify it gets called
        order_id = 1
        amount = 200
        payment_method = 'credit_card'

        process_payment_task.delay(order_id, amount, payment_method)

        mock_process_payment.assert_called_with(order_id, amount, payment_method)
