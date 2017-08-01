from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    nickname = models.CharField(unique=True, max_length=32, default=None)
    phone_number=models.CharField(max_length=20, validators=[RegexValidator(r'^010[1-9]\d{7}$')], help_text='01012341234')
    address=models.CharField(max_length=50,help_text='xx시 xx구')

