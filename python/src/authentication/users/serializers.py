from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'first_name', 'last_name', 'username', 'email', 'address', 'city', 'postal_code', 'password', 'email_verified', 'date_joined', 'slug', 'last_login', 'is_active', 'is_staff', 'is_superuser']
        lookup_field = 'uuid'
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance       