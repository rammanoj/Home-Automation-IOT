from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from . import serializers
from rest_framework.pagination import DjangoPaginator
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView, \
    UpdateAPIView
from . import models
from django.contrib.auth.models import User
# Create your views here.


# model 'Home' generic views

class HomeListView(ListAPIView):
    serializer_class = serializers.HomeListSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return models.Home.objects.none()
        return models.Home.objects.filter(user=self.request.user)


class HomeDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.HomeSerializer
    permission_classes = []
    authentication_classes = []

    def get_queryset(self):
        user = User.objects.get(username='rammanoj')
        return models.Home.objects.filter(user=user)


class HomeCreateView(CreateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = serializers.HomeSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Response({'error': 'please login first.'})
        return User.objects.filter(user=self.request.user)


# model 'Switch' generic views

class SwitchCreateView(CreateAPIView):
    serializer_class = serializers.SwitchSerializer
    queryset = models.Switch.objects.all()


class SwitchListView(ListAPIView):
    serializer_class = serializers.SwitchSerializer

    def get_queryset(self):
        home_id = self.kwargs.get('home_id', None)
        if home_id is None or int(home_id) < 0:
            return models.Switch.objects.none()
        try:
            query = models.Switch.objects.filter(home=get_object_or_404(models.Home, pk=home_id))
        except ObjectDoesNotExist:
            return models.Switch.objects.none()
        return query


class SwitchUpdateView(UpdateAPIView):
    serializer_class = serializers.SwitchSerializer

    def get_queryset(self):
        pass

# API views to handle gas leakage, Fire accident and Automated setting of AC on decreasing temperature





