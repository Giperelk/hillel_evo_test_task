from rest_framework import serializers
from account.models import User


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'last_login', 'last_request']
