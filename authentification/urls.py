from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
  path('',views.sign_in,name='signin'),
  path('signup',views.sign_up,name='signup'),
  path('home/',views.home,name='home'),
  path('sendemail/',views.sendEmail,name='sendEmail'),
  path('reset_password/',auth_views.PasswordResetView.as_view(email_template_name='password_reset_email_custom.html',html_email_template_name='password_reset_email_custom.html'),name='reset_password'),
  path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
  path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
  path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete')
]
