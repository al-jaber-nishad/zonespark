from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.views.category_views import CategoryViewSet
from product.views.product_views import ProductViewSet
from product.views.stock_views import StockViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'stocks', StockViewSet, basename='stock')

urlpatterns = [
    path('', include(router.urls)),
]
