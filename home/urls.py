from django.conf.urls import url
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    # model 'Home' urls
    url(r'^home/create/$', views.HomeCreateView.as_view(), name='create-home'),
    url(r'^home/$', views.HomeListView.as_view(), name='list-home'),
    url(r'^home/(?P<pk>\d+)/$', views.HomeDetailView.as_view(), name='detail-home'),

    # model 'Switch' urls
    url(r'^switch/create/$', views.SwitchCreateView.as_view(), name='create-switch'),
    url(r'^switch/(?P<pk>\d+)/$', views.SwitchDetailView.as_view(), name='switch-detail'),
    url(r'^switch/list/(?P<home_id>\d+)/$', views.SwitchListView.as_view(), name='list-switch'),
]