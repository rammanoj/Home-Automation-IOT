from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Home(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    temperature = models.FloatField(default=25, null=True, blank=True)
    humidity = models.FloatField(default=40, null=True, blank=True)
    temperature_user_set = models.FloatField(default=None, null=True, blank=True)

    def __str__(self):
        return "id:" + str(self.pk) + " " + self.user.username


class Switch(models.Model):

    SWITCH_STATUS = (
        ('on', 'switch is oN'),
        ('off', 'switch is oFF'),
    )

    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    switch_name = models.CharField(max_length=200, null=True, blank=True)
    switch_status = models.CharField(choices=SWITCH_STATUS, max_length=3, default='off')

    def __str__(self):
        return self.switch_name


