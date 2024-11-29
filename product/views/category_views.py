from rest_framework.permissions import IsAuthenticatedOrReadOnly
from product.models import Category
from product.serializers.category_serializer import CategorySerializer
from product.base import BaseModelViewSet

class CategoryViewSet(BaseModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
