from django.db import models

# Create your models here.
class Account(models.Model):
    account_number = models.CharField(max_length = 20)
    balance = models.FloatField(default = 0)

    def __str__(self):
        return self.account_number


class Transaction(models.Model):
    from_account = models.ForeignKey(Account, related_name = 'sent', on_delete = models.CASCADE)
    to_account = models.ForeignKey(Account, related_name = 'received', on_delete = models.CASCADE)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add = True)


class Product(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField()