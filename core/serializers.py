from rest_framework import serializers
from .models import Transaction, Account, Product


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    recent_transactions =  TransactionSerializer(many = True, read_only = True, source = 'sent')

    class Meta:
        model = Account
        fields = ['id', 'account_number', 'balance', 'recent_transactions']

    def get_recent_transactions(self, obj):
        transactions = Transaction.objects.filter(from_account = obj) | Transaction.objects.filter(to_account = obj)
        return TransactionSerializer(transactions.order_by('-id')[:5], many = True).data
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'