from rest_framework.routers import DefaultRouter

from products.viewsets import ProductViewSet, ProductGenericViewSet

router = DefaultRouter()
# router.register('products-abc', ProductViewSet, basename='products') # url path 지정
router.register('products', ProductGenericViewSet, basename='products') # GenericViewset 사용

urlpatterns = router.urls