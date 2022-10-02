from django.conf import settings
from django.db import models
from django.db.models import Q

User = settings.AUTH_USER_MODEL # auth.User


class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)
    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct() # 중복 제거
        return qs


class ProductManager(models.Manager): ## 잠재적으로 다른 데이터베이스도 사용할 수 있다.
    def get_queryset(self, *args, **kwargs):
        return ProductQuerySet(self.model, using=self._db) ## 새로운 제품 queryset 반환 _db는 기본 db

    def search(self, query, user=None):
        # return Product.objects.filter(public=True).filter(title__icontains=query)
        return self.get_queryset().search(query, user=user)


class Product(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99) # 소수점 필드
    public = models.BooleanField(default=True)

    objects = ProductManager() ## 호출할 수 있게
    @property
    def sale_price(self):
        return "%.2f" % (float(self.price) * 0.8)

    def get_discount(self):
        return '122'
