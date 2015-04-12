from django.db import models
from djmoney.models.fields import MoneyField


class Transaction(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    timestamp = models.DateTimeField()
    type = models.CharField(max_length=32)
    from_email = models.EmailField()
    to_email = models.EmailField()
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=30)
    amount = MoneyField(max_digits=10, decimal_places=2)
    fee_amount = MoneyField(max_digits=10, decimal_places=2)
    net_amount = MoneyField(max_digits=10, decimal_places=2)
    reference = models.ForeignKey('Transaction', null=True)
    # The following is a PS:One account balance, not a user balance
    balance = MoneyField(max_digits=10, decimal_places=2)

    def __str__(self)
        return 'id=%s, timestamp=%s, type=%s, from_email=%s, to_email=%s, name=%s, status=%s, amount=%s, fee=%s, net=%s, balance=%s' % (
        self.id, self.timestamp, self.type, self.from_email, self.to_email, self.name, self.status, self.amount, self.fee_amount, self.net_amount, self.balance)
