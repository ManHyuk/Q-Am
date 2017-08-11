from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import validate_email
from qna.models import Answer
from django.utils import timezone
from django.core.validators import RegexValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.contrib.auth.forms import AuthenticationForm


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=10)
    nickname = models.CharField(unique=True, max_length=32, default=None)
    phone_number = models.CharField(max_length=20,validators=[RegexValidator(r'^010[1-9]\d{7}$')])
    email = models.EmailField(max_length=100)
    img = ProcessedImageField(
        upload_to='blog/%Y/%m/%d',
        blank=True,
        null=True,
        processors=[Thumbnail(150, 150)],  # 처리할 작업목록
        format='JPEG',
        options={'quality': 80}
    )




