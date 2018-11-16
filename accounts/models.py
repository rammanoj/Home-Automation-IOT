from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class MailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.TextField(null=True, blank=True)
    link_expire = models.DateTimeField(default=timezone.now())
    request_type = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.user.username

    # 'link' is to implement the operations like password_change, user registration etc