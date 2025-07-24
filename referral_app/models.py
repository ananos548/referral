from django.db import models

class Profile(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    auth_code = models.CharField(max_length=4, blank=True)
    invite_code = models.CharField(max_length=6, unique=True, null=True)
    referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='referrals')

    def __str__(self):
        return f"{self.invite_code}"