from django.urls import path
from authentication.views import user_views as views

urlpatterns = [
    path('api/v1/user/register/', views.register_user),

    path('api/v1/user/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]