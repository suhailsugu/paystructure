from rest_framework import serializers
from apps.user.models import Users



class LoginResponseSchema(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = [
            "id",
            "email",
            "name",
            "username",
            "is_admin",
            "is_active",
            "is_verified",
            "is_superuser",
            "is_staff",
        ]