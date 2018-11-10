from rest_framework import serializers
from . import models
from django.db import IntegrityError
from django.contrib.auth.models import User


class HomeSerializer(serializers.ModelSerializer):

    def validate_name(self, name):

        if len(name) < 8:
            raise serializers.ValidationError('min length of 8 for home name')

        return name

    class Meta:
        model = models.Home
        fields = ('pk', 'name', 'temperature', 'humidity')
        read_only_fields = ('pk', 'temperature', 'humidity')


class SwitchSerializer(serializers.ModelSerializer):

    SWITCH_STATUS = (
        ('on', 'switch is ON'),
        ('off', 'switch is OFF'),
    )

    switch_name = serializers.CharField(max_length=50, required=True)
    switch_status = serializers.ChoiceField(SWITCH_STATUS, required=False)

    def validate_switch_name(self, name):
        if len(name) < 5:
            raise serializers.ValidationError('Name should be atleast 8 in length')
        if models.Switch.objects.filter(switch_name=name).exists():
            raise serializers.ValidationError('switch name already taken by another user')
        return name

    class Meta:
        model = models.Switch
        fields = ('pk', 'switch_name', 'switch_status')
        read_only_fields = ('pk',)


class HomeListSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    name = serializers.CharField()

