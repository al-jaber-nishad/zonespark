from rest_framework.permissions import IsAuthenticatedOrReadOnly
from product.models import Product
from product.serializers.product_serializer import ProductSerializer
from product.base import BaseModelViewSet

class ProductViewSet(BaseModelViewSet):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
