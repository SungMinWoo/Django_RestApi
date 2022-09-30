from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Product

# def validate_title(value):  # title은 이전에 입력된 값
#     qs = Product.objects.filter(
#         title__exact=value)  # exact 정확히 일치하는 데이터 찾기, iexact 대소문자 구분하지 않고 정확히 일치하는 값 찾기
#     if qs.exists():
#         raise serializers.ValidationError(f"{value} is already a product name.")
#     return value


def validate_title_no_hello(value):
    if 'hello' in value.lower():
        raise serializers.ValidationError(f"Hello is not allowed")
    return value

unique_product_title = UniqueValidator(queryset=Product.objects.all())