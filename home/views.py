from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from rest_framework import status
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

    def get_queryset(self):
        return models.Home.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        super(HomeDetailView, self).delete(request, *args, **kwargs)
        return Response({'message': 'successfully deleted', 'success': 1}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        instance = super(HomeDetailView, self).partial_update(request, *args, **kwargs)
        instance.data['success'] = 1
        instance.data['message'] = 'successfully updated'
        return instance


class HomeCreateView(CreateAPIView):
    serializer_class = serializers.HomeSerializer

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response({'message': 'created home'})
        else:
            return Response({'error': serializer.errors})


class SwitchCreateView(CreateAPIView):
    serializer_class = serializers.SwitchSerializer
    queryset = models.Switch.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            home = models.Home.objects.get(pk=request.data['home'])
        except ObjectDoesNotExist:
            return Response({'error': 'Home is not found'})

        if home not in request.user.home_set.all():
            return Response({'error': 'permission denied'})

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['home'] = home
            serializer.validated_data['switch_status'] = 'off'
            serializer.save()
            return Response({'message': 'successfully updated', 'success': 1})
        else:
            return Response({'error': serializer.errors})


class SwitchListView(ListAPIView):
    serializer_class = serializers.SwitchSerializer

    lookup_field = 'home_id'

    def get_queryset(self):
        home_id = self.kwargs.get('home_id', None)
        if home_id is None or int(home_id) < 0:
            return models.Switch.objects.none()
        try:
            query = models.Switch.objects.filter(home=models.Home.objects.filter(pk=home_id))
        except ObjectDoesNotExist:
            return models.Switch.objects.none()
        return query

    def get(self, request, *args, **kwargs):
        print(self.get_object().home.user)
        print(request.user)
        if request.user is not self.get_object().home.user:
            return Response({'error': 'permission denied'})
        return super(SwitchListView, self).get(request, *args, **kwargs)


class SwitchUpdateView(UpdateAPIView):
    serializer_class = serializers.SwitchSerializer

    def get_queryset(self):
        pass

# API views to handle gas leakage, Fire accident and Automated setting of AC on decreasing temperature





