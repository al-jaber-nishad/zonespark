from rest_framework.permissions import IsAuthenticated
from product.models import Stock
from product.serializers.stock_serializer import StockSerializer
from product.base import BaseModelViewSet

class StockViewSet(BaseModelViewSet):
    queryset = Stock.objects.select_related('product')
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]
