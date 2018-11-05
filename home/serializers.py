from rest_framework import serializers
from . import models
from django.db import IntegrityError
from django.contrib.auth.models import User


class HomeSerializer(serializers.ModelSerializer):

    def create(self, validated_data):

        user = User.objects.get(username=self.request.user)
        models.Home.objects.create(user=user, temperature=validated_data['temperature'],
                                   humidity=validated_data['humidity'])
        return validated_data

    class Meta:
        model = models.Home
        fields = ('pk', 'name', 'temperature', 'humidity')


class SwitchSerializer(serializers.ModelSerializer):

    SWITCH_STATUS = (
        ('on', 'switch is ON'),
        ('off', 'switch is OFF'),
    )

    switch_name = serializers.CharField(max_length=50, required=True)
    switch_status = serializers.ChoiceField(SWITCH_STATUS)

    def create(self, validated_data):
        user = User.objects.get(username='rammanoj')
        home = models.Home.objects.get(user=user)
        models.Switch.objects.create(home=home, switch_name=validated_data['switch_name'],
                                     switch_status=validated_data['switch_status'])
        return validated_data

    class Meta:
        model = models.Switch
        fields = ('switch_name', 'switch_status')


class HomeListSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    name = serializers.CharField()

