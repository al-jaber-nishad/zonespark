from django.contrib.auth import get_user_model
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from authentication.models import Role
from authentication.serializers import AdminUserSerializer, UserLogInSerializer
from authentication.utils import generate_unique_username

# Get the User model
User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT Token serializer to include additional user data in the response.
    """
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            user_data = UserLogInSerializer(self.user).data
            data.update(user_data)
            data['user_id'] = self.user.id
            return data
        except Exception as e:
            raise ValidationError({'detail': str(e)}, code=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT Token View to use the custom serializer.
    """
    serializer_class = CustomTokenObtainPairSerializer


class RegisterUserView(generics.CreateAPIView):
    """
    API view for user registration.
    """
    serializer_class = AdminUserSerializer

    @extend_schema(request=AdminUserSerializer, responses=AdminUserSerializer)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')

        # Check for existing email
        if email and User.objects.filter(email=email).exists():
            return Response({'detail': "Email already exists!"}, status=status.HTTP_400_BAD_REQUEST)

        # Filter out invalid or restricted values
        restricted_values = ('', 'undefined', ' ', 0, '0', None)
        filtered_data = {key: value for key, value in data.items() if value not in restricted_values}

        # Assign default role and generate unique username
        try:
            filtered_data['role'] = Role.objects.get(name='CUSTOMER').id
        except Role.DoesNotExist:
            return Response({"detail": "Default role 'CUSTOMER' not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        filtered_data['username'] = generate_unique_username(data.get('first_name') or data.get('email') or "user")

        serializer = self.get_serializer(data=filtered_data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response({"user": user.id}, status=status.HTTP_201_CREATED)
            except Exception as e:
                transaction.set_rollback(True)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
