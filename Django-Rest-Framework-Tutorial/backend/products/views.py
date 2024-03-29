from rest_framework import generics, mixins, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from api.mixins import StaffEditorPermissionMixin, UserQuerysetMixin
from api.permissions import IsStaffEditorPermission
from .models import Product
from .serializers import ProductSerializers


class ProductListCreateAPIView(
    UserQuerysetMixin,
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView): # 리스트를 보여주고 만들 수 있는 class
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    allow_staff_view = False
    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        # email = serializer.validated_data.pop('email') # 실제로 저장하진 않지만 입력하는 값을 가져올 수 있음
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content) ## form.save() model.save()와 같다.

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs) # product의 list를 반환함
    #     request = self.request
    #     user = request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     return qs.filter(user=request.user)

class ProductDetailAPIView(
    UserQuerysetMixin,
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    # lookup_field = 'pk' # 원하는 필드를 설정하는 곳


class ProductUpdateAPIView(
    UserQuerysetMixin,
    StaffEditorPermissionMixin,
    generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title


class ProductDestroyAPIView(
    UserQuerysetMixin,
    StaffEditorPermissionMixin,
    generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


class ProductMixinView(mixins.CreateModelMixin, mixins.ListModelMixin, # 혼합 class view
                       mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    lookup_field = 'pk'
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

    def get(self, request, *args, **kwargs): # get 메소드일때
        # print(args, kwargs) ## () {'pk': 10}
        pk = kwargs.get('pk')
        if pk is not None: # pk 값이 넘어왔다면 detail로 넘겨줌
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')
        if content is None:
            content = title
        serializer.save(content=content)


# @api_view(['GET', 'POST'])
# def product_alt_view(request, pk=None, *args, **kwargs):
#     method = request.method
#
#     if method == "GET":
#         if pk is not None:
#             queryset = Product.objects.filter(pk=pk)
#             obj = get_object_or_404(Product, pk=pk)
#             data = ProductSerializers(obj, many=False).data
#             return Response(data)
#         else:
#             queryset = Product.objects.all()
#             data = ProductSerializers(queryset, many=True).data
#             # 중복 값에 대해 list로 받고자하는 경우 True 혹은 다수의 데이터 형태를 serialize화 하고자 할때
#             return Response(data)
#     if method == "POST":
#         serializer = ProductSerializers(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             title = serializer.validated_data.get('title')
#             content = serializer.validated_data.get('content')
#             if content is None:
#                 content = title
#             serializer.save(content=content)
#             data = serializer.data
#             return Response(data)
#         return Response({'incalid':'not good data'}, status=400)
