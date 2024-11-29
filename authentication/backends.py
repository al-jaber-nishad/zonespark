from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q




class EmailorPhoneModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check if request is DRF's request or regular Django request
            
        if username.startswith('+'):
            username = username
        elif not username.startswith('+') and username.isdigit():
            username = '+88' +  username[-11:]

        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(Q(username__exact=username) | Q(primary_phone__exact=username) | Q(email__exact=username))
        except UserModel.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user

        return None

