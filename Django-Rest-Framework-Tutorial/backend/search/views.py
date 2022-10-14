from rest_framework import generics
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializers


class SearchListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q') # q는 검색할 keyword
        results = Product.objects.none() # none을 활용해 데이터베이스에 도달하지 않음, 결과가 없을 것으로 생각되면 사용
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            results = qs.search(q, user=user)
            print(results)
        return results

# class SearchListView(generics.GenericAPIView):
#     def get(self, request, *args, **kwargs):
#         user = None
#         if request.user.is_authenticated:
#             user = request.user.username
#         query = request.GET.get('q')
#         public = str(request.GET.get('public')) != "0"
#         tag = request.GET.get('tag') or None
#         if not query:
#             return Response('', status=400)
#         results = client.perform_search(query, tags=tag, user=user, public=public)
#         return Response(results)
