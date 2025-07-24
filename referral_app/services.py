import random
import string

from referral_app import models

def generate_invite_code():
    return ''.join(random.choices(string.digits + string.ascii_letters, k=6))


def generate_auth_code():
    return ''.join(random.choices(string.digits, k=4))

def create_or_get_user_by_phone(phone: str) -> tuple[models.Profile, bool]:
    user, created = models.Profile.objects.get_or_create(phone=phone)
    if created:
        user.auth_code = generate_auth_code()
        user.invite_code = generate_invite_code()
        user.save()
    return user, created
