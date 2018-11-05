from django.conf.urls import url
from . import views
from rest_framework import routers
#
# router = routers.DefaultRouter()
# router.register(r'users', UserView, basename='user', action='list')
# router.register(r'users/(?P<pk>\d+)/$', basename='users-detail', action='detail')

urlpatterns = [
    url(r'^create/$', views.UserCreateView.as_view(), name='create-user'),
    url(r'^(?P<pk>\d+)/$', views.UserView.as_view(), name='list-user'),
    url(r'^login/$', views.login, name='login')
]

# urlpatterns += router.urls