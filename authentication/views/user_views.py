from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from authentication.models import  Role
from authentication.serializers import AdminUserSerializer, UserLogInSerializer

from authentication.utils import generate_unique_username

# Get the User model
User = get_user_model()


# Custom JWT Token Serializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
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
        except PermissionDenied as e:
            raise ValidationError({'detail': str(e)}, code=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            raise ValidationError({'detail': str(e)}, code=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT Token View to use the custom serializer.
    """
    serializer_class = MyTokenObtainPairSerializer



# User Registration View
@extend_schema(request=AdminUserSerializer, responses=AdminUserSerializer)
@api_view(['POST'])
@transaction.atomic
def register_user(request):
    """
    Registers a new user and assigns a default role.
    """
    data = request.data
    email = data.get('email')

    if email and User.objects.filter(email=email).exists():
        return Response({'detail': "Email already exists!"}, status=status.HTTP_400_BAD_REQUEST)

    # Filter out invalid or restricted values
    restricted_values = ('', 'undefined', ' ', 0, '0', None)
    filtered_data = {key: value for key, value in data.items() if value not in restricted_values}
    filtered_data['role'] = Role.objects.get(name='CUSTOMER').id

    # Generate unique username
    filtered_data['username'] = generate_unique_username(data.get('first_name') or data.get('email') or "user")

    serializer = AdminUserSerializer(data=filtered_data)
    try:
        if serializer.is_valid():
            user = serializer.save()
            
            return Response({"user": user.id}, status=status.HTTP_201_CREATED)
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        transaction.set_rollback(True)
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
