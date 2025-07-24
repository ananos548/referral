from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Profile

class UserProfileSerializer(serializers.ModelSerializer):
    referred_users = serializers.SerializerMethodField()
    referred_by_invite_code = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'id', 'phone', 'auth_code', 'invite_code',
            'referred_by', 'referred_by_invite_code', 'referred_users'
        )

    def get_referred_users(self, obj):
        referred_users = Profile.objects.filter(referred_by=obj)
        return [user.phone for user in referred_users]

    def get_referred_by_invite_code(self, obj):
        return obj.referred_by.invite_code if obj.referred_by else None
