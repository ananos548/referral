from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Profile
from .serializers import UserProfileSerializer
from .services import *




class UserProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Создаёт пользователя с переданным телефоном, если он не существует.
        Возвращает auth_code.
        """
        phone = request.data.get('phone')
        if not phone:
            return Response({"message": "Phone is required"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = create_or_get_user_by_phone(phone)

        if created:
            return Response({
                "success": True,
                "message": "User created",
                "data": {
                    "auth_code": user.auth_code
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "User already exists"
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """
        Проверяет auth_code для пользователя по телефону.
        При успехе — очищает код и генерирует новый invite_code.
        """
        phone = request.data.get('phone')
        entered_auth_code = request.data.get('auth_code')

        if not phone or not entered_auth_code:
            return Response({"message": "Phone and auth_code required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile = Profile.objects.get(phone=phone, auth_code=entered_auth_code)
        except Profile.DoesNotExist:
            return Response({"message": "Verification failed"}, status=status.HTTP_400_BAD_REQUEST)

        profile.auth_code = ''
        profile.invite_code = generate_invite_code()
        profile.save()

        return Response({
            "success": True,
            "message": "User verified",
            "data": {
                "invite_code": profile.invite_code
            }
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def activate_invite_code(self, request):
        """
        Пользователь вводит чужой invite_code. Сохраняем, кто его пригласил.
        """
        phone = request.data.get('phone')
        invite_code = request.data.get('invite_code')

        if not phone or not invite_code:
            return Response({"message": "Phone and invite_code are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Profile.objects.get(phone=phone)
        except Profile.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            referrer = Profile.objects.get(invite_code=invite_code)
        except Profile.DoesNotExist:
            return Response({"message": "Invalid invite code"}, status=status.HTTP_400_BAD_REQUEST)

        # Нельзя пригласить самого себя
        if referrer == user:
            return Response({"message": "You cannot refer yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Нельзя использовать код дважды
        if user.referred_by is not None:
            return Response({"message": "Invite code already used."}, status=status.HTTP_400_BAD_REQUEST)

        user.referred_by = referrer
        user.save()

        return Response({
            "success": True,
            "message": "Invite code activated",
            "data": {
                "referrer_phone": referrer.phone
            }
        }, status=status.HTTP_200_OK)
