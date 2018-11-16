from django.conf.urls import url
from . import views
from rest_framework import routers
#
# router = routers.DefaultRouter()
# router.register(r'users', UserView, basename='user', action='list')
# router.register(r'users/(?P<pk>\d+)/$', basename='users-detail', action='detail')

urlpatterns = [
    # verifying mail
    url(r'^mailverify/(?P<verify_id>\w+)/$', views.mail_verify, name='verify-mail'),
    url(r'^forgot_password_reset/$', views.password_reset, name='forgot-password-reset'),

    # User model operations
    url(r'^(?P<pk>\d+)/$', views.UserView.as_view(), name='user-detial'),
    url(r'^create/$', views.UserCreateView.as_view(), name='create-user'),
    url(r'^forgot_password_update/(?P<link>\w+)/$', views.ForgotPasswordResetView.as_view(), name='forgot-password-update'),
    url(r'^password_update/(?P<pk>\d+)/$', views.PasswordResetView.as_view(), name='password-update'),
    url(r'^user_update/(?P<pk>\d+)/$', views.UserUpdateView.as_view(), name='user-update'),

    # login and logout operations
    url(r'^login/$', views.login, name='login'),
    url('^logout/$', views.Logout.as_view(), name='logout'),
]


# user update


# three kinds of mail verifications
# 1. password forget - 2
# 2. email change - 1
# 3. user registration - 0

# also check for the expiry of the link