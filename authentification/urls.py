from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from allauth.account import views as allauth_views


urlpatterns = [
  path('',views.home_page,name='home_page'),
  path('sign_in',views.sign_in,name='signin'),
  path('signup',views.sign_up,name='signup'),
  path('home/',views.home,name='home'),
  path('sendemail/',views.sendEmail,name='sendEmail'),
  path('password/reset/', allauth_views.PasswordResetView.as_view(), name='account_reset_password'),
  path('password/reset/done/', allauth_views.PasswordResetDoneView.as_view(), name='account_reset_password_done'),
  path('password/reset/key/<uidb36>/<key>/', allauth_views.PasswordResetFromKeyView.as_view(), name='account_reset_password_from_key'),
  path('password/reset/key/done/', allauth_views.PasswordResetFromKeyDoneView.as_view(), name='account_reset_password_from_key_done'),
  path('logout/',views.logout_view,name='logout'),
  path('profile/',views.profile,name='profile')
]
