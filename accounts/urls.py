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
    url(r'^login/$', views.login, name='login'),
    url(r'^mailverify/(?P<verify_id>\w+)/$', views.mail_verify, name='verify-mail'),
    url(r'password_reset/$', views.password_reset, name='password-reset'),
    url(r'^password_update/(?P<link>\w+)/$', views.PasswordReset.as_view(), name='passwrod-update'),
    url(r'^user_update/(?P<pk>\d+)/$', views.UserUpdateView.as_view(), name='user-update'),
    url('^logout/$', views.Logout.as_view(), name='logout'),
]

# urlpatterns += router.urls