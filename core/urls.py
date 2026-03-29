from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, TransactionViewSet, ProductViewSet

router = DefaultRouter()
router.register('accounts', AccountViewSet)
router.register('transactions', TransactionViewSet)
router.register('products', ProductViewSet)

urlpatterns = router.urls
