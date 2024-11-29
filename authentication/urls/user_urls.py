from django.urls import path
from authentication.views import user_views as views


urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register_user'),

    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]