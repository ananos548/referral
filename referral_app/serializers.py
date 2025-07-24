from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Profile

class UserProfileSerializer(ModelSerializer):
    referred_users = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id', 'phone', 'auth_code', 'invite_code', 'referred_by', 'referred_users')

    def get_referred_users(self, obj):
        referred_users = Profile.objects.filter(referred_by=obj.id)
        return (user.phone for user in referred_users)