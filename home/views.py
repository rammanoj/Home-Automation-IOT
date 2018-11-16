import hashlib
import requests, json
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import serializers
from accounts import mails_content
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.mixins import UpdateModelMixin
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
            serializer.validated_data['esp_code'] = hashlib.sha256(serializer.validated_data['name']
                                                                   .encode('utf-8')).hexdigest()
            serializer.save()
            data = mails_content.esp_content
            data['message'] += hashlib.sha256(serializer.validated_data['name'].encode('utf-8')).hexdigest()
            send_mail(subject=data['subject'], message=data['message'], from_email=data['from_mail'],
                      recipient_list=[self.request.user.email])
            return Response({'message': 'created home, check your mail'})
        else:
            return Response({'error': serializer.errors})


class SwitchCreateView(CreateAPIView):
    serializer_class = serializers.SwitchSerializer
    queryset = models.Switch.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            home = request.user.home_set.get(pk=request.data['home'])
        except ObjectDoesNotExist:
            return Response({'error': 'Home is not found'})

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['home'] = home
            serializer.validated_data['switch_status'] = 'off'
            serializer.save()
            return Response({'message': 'successfully updated', 'success': 1})
        else:
            return Response({'error': serializer.errors})


class SwitchListView(UpdateModelMixin, ListAPIView):
    serializer_class = serializers.SwitchSerializer
    lookup_field = 'home_id'

    def get_queryset(self):
        home_id = self.kwargs.get('home_id', None)
        if home_id is None or int(home_id) < 0 or \
                self.request.user.pk != models.Home.objects.filter(pk=home_id)[0].user.pk:
            return models.Switch.objects.none()
        query = models.Switch.objects.filter(home=models.Home.objects.filter(pk=home_id))
        return query

    def get(self, request, *args, **kwargs):
        return super(SwitchListView, self).get(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        data = request.data['data']
        for i in data:
            query = self.get_queryset().filter(i['pk'])
            if query.exists():
                query.switch_status = i['switch_status']
                query.save()

        return Response({'message': 'successfully updated switch!'})


class SwitchDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.SwitchSerializer

    def get_queryset(self):
        home = self.request.user.home_set.all()
        print(self.kwargs['pk'])
        switch = models.Switch.objects.filter(pk=self.kwargs['pk'])
        if not switch.exists() or switch[0].home not in home:
            return models.Switch.objects.none()
        return switch

    def delete(self, request, *args, **kwargs):
        super(SwitchDetailView, self).delete(request, *args, **kwargs)
        return Response({'message': 'Switch successfully deleted'})


@api_view(['POST'])
@permission_classes((AllowAny,))
def update_home(request):
    # Only esp board has the access to it.

    # store the temperature and humidity values to the Home modal
    serializer = serializers.HomeUpdateSerializer(data=request.data)
    if serializer.is_valid():
        queryset = models.Home.objects.filter(esp_code=serializer.validated_data['esp_code'])
        if not queryset.exists():
            return Response({'error': 'error'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        query = queryset[0]
        query.temperature = serializer.validated_data['temperature']
        query.humidity = serializer.validated_data['humidity']
        query.save()
        return Response({'message': 'success'}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({'error': 'error'}, status=status.HTTP_304_NOT_MODIFIED)


@api_view(['POST'])
@permission_classes([AllowAny])
def security_check(request):
    # check for fire accident or gas leakage at the house
    queryset = models.Home.objects.filter(esp_code=request.data['esp_code'])
    if not queryset.exists():
        return Response({'error': 'error'}, status=status.HTTP_400_BAD_REQUEST)

    location = requests.get('http://api.ipstack.com/' + request.data['ip'] + '?access_key=' +
                            mails_content.access_key)
    location = json.loads(location.text)
    print(location['ip'])
    if request.data['fire'] == 1:
        # send mail to nearby fire station
        data = mails_content.fire_content
        mail = 'firestationmail@gmail.com'
        data['message'] += 'city in ' + location['city'] + '\n\n latitude: ' + str(location['latitude'])\
                           + '\n\n longitude: ' + str(location['longitude'])
        send_mail(data['subject'], data['message'], data['from_mail'], [mail])
    elif request.data['gas_leak'] == 1:
        # send mail by getting the house location on gas leakage.
        data = mails_content.gas_leak_content
        data['message'] += 'city in ' + location['city'] + '\n\n latitude: ' + str(location['latitude'])\
                           + '\n\n longitude: ' + str(location['longitude'])
        send_mail(data['subject'], data['message'], data['from_mail'], [queryset[0].user.email])

    return Response({'success': 'success'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def temperature_control(request):
    queryset = models.Home.objects.filter(esp_code=request.data['esp_code'])
    if not queryset.exists():
        return Response({'error': 'error'}, status=status.HTTP_400_BAD_REQUEST)

    rv = {}
    if queryset[0].temperature > queryset[0].temperature_user_set:
        rv['ac'] = 1 # ON AC to bring down room temperature
    elif queryset[0].temperature < queryset[0].temperature_user_set:
        rv['ac'] = -1 # ON Heater to rise up room temperature
    else:
        rv['ac'] = 0 # No need to on either of both

    return Response({'data': json.dumps(rv)}, status=status.HTTP_200_OK)


def esp_switch_update(request):

    # switch_status can assume values 0, 1
    # 0 ->no user update
    # 1 -> user updates status

    queryset = models.Home.objects.filter(esp_code=request['esp_code'])
    if not queryset.exists():
        return Response({'error': 'error'}, status=status.HTTP_400_BAD_REQUEST)

    switches = queryset.switch_set.all()
    j = 0
    rv = {}
    for i in switches:
        query = switches.objects.get(relay=request.data[j]['relay'])
        rv[j]['esp_code'] = request.data[j]['esp_code']

        if query.switch_status == request.data[j]['switch_status']:
            rv[j]['switch_status'] = request.data[j]['switch_status']

        elif query.user_status == 1:
            query.user_status = 0
            rv[j]['switch_status'] = query.switch_status

        elif query.switch_status != request.data[j]['switch_status']:
            query.switch_status = request.data[j]['switch_status']
            rv[j]['switch_status'] = request.data[j]['switch_status']

        query.save()

    return Response({'data': json.dumps(rv)}, status=status.HTTP_200_OK)


# API views to handle gas leakage, Fire accident and Automated setting of AC on decreasing temperature

# handle these things:
# send mail after creating a home about the esp code  --done --tested
# 1. temperature and humidity update by esp --done --tested
# 2. list delete view for switches --not yet done :(
# 3. gas, fire and smoke handle and send corresponding mail --done
# 4. ON AC signal with temperature > temp_set --done



# haven't checked the code of the esp_switch_update
# also there is a need of update to the location api
# also update the code of the listupdate api view to add the patch method
# then go to the user details updation

# and finally write the documentation to the entire api and start with react creating the frontend \
# along with the arduino board




