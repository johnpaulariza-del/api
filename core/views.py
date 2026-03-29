from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django.db import transaction
from .models import Transaction, Account, Product
from .serializers import TransactionSerializer, AccountSerializer, ProductSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['amount', 'from_account__account_number', 'to_account__account_number']

    def create(self, request):
        from_id = request.data.get('from_account')
        to_id = request.data.get('to_account')
        amount = float(request.data.get('amount', 0))

        if amount <= 0:
            return Response({"error": "Amount must be > 0"}, status =  400)
        
        try:
            with transaction.atomic():
                sender =  Account.objects.select_for_update().get(id = from_id)
                receiver = Account.objects.select_for_update().get(id = to_id)

                if sender.balance < amount:
                    return Response({"error": "Insufficient funds"}, status = 400)
                
                sender.balance -= amount
                receiver.balance -= amount

                sender.save()
                receiver.save()

                txn = Transaction.objects.create(
                    from_account = sender,
                    to_account =  receiver,
                    amount = amount
                )

                return Response(TransactionSerializer(txn).data, status = 201)
        
        except Exception as e:
            return Response({"error": str(e)}, status = 500)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer