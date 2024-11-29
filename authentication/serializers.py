from django_currentuser.middleware import get_current_authenticated_user
from rest_framework import serializers
from authentication.models import User


class UserLogInSerializer(serializers.ModelSerializer):
	permissions = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'role', 'permissions']

	def get_permissions(self, obj):
		return obj.role.permissions.values_list('code', flat=True)


class UserListSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ['password', 'phone_otp', 'is_active']
		extra_kwargs = {
			'password': {
				'write_only': True,
				'required': False,
			},
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}


class AdminUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'
		extra_kwargs = {
			'password': {
				'write_only': True,
				'required': False,
			},
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}

	def create(self, validated_data):
		modelObject = super().create(validated_data=validated_data)
		modelObject.set_password(validated_data["password"])
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.created_by = user
		modelObject.save()
		return modelObject
	
	def update(self, instance, validated_data):
		modelObject = super().update(instance=instance, validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.updated_by = user
		modelObject.save()
		return modelObject
