from rest_framework import serializers
from rest_framework.reverse import reverse

from api.serializers import UserPublicSerializer
from .validators import validate_title_no_hello, unique_product_title
from .models import Product


class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
        read_only=True
    )
    title = serializers.CharField(read_only=True)


class ProductSerializers(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user', read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True) ## viewset
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
    )
    title = serializers.CharField(validators=[validate_title_no_hello, unique_product_title])
    class Meta:
        model = Product
        fields = [
            'owner',
            'url',
            'edit_url', ## viewset
            'pk',
            'title',
            'content',
            'price',
            'sale_price',
            'public',
        ]
    def get_my_user_data(self, obj):
        return {
            'username': obj.user.username
        }
    # def validate_title(self, value): # title은 이전에 입력된 값
    #     request = self.context.get('request')
    #     user = request.user
    #     qs = Product.objects.filter(user=user, title__exact=value) # exact 정확히 일치하는 데이터 찾기, iexact 대소문자 구분하지 않고 정확히 일치하는 값 찾기
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a product name.")
    #     return value
    # def create(self, validated_data):
    #     # return Product.objects.create(**validated_data)
    #     email = validated_data.pop('email')
    #     obj = super().create(validated_data)
    #     return obj
    #
    # def update(self, instance, validated_data):
    #     email = validated_data.pop('email')
    #     return super().update(instance, validated_data)

    def get_edit_url(self, obj): ## viewset
        # return f'/api/v2/products/{obj.pk}/'
        request = self.context.get('request') # self.request
        if request is None:
            return None
        return reverse("product-edit", kwargs={'pk': obj.pk}, request=request)
