from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from allauth.account import views as allauth_views


urlpatterns = [
  path('',views.home_page,name='home_page'),
  path('sign_in',views.sign_in,name='signin'),
  path('signup',views.sign_up,name='signup'),
  path('sign_client',views.sign_client,name='sign_client'),
  path('home/',views.home,name='home'),
  path('sendemail/',views.sendEmail,name='sendEmail'),
  path('password/reset/', allauth_views.PasswordResetView.as_view(), name='account_reset_password'),
  path('password/reset/done/', allauth_views.PasswordResetDoneView.as_view(), name='account_reset_password_done'),
  path('password/reset/key/<uidb36>/<key>/', allauth_views.PasswordResetFromKeyView.as_view(), name='account_reset_password_from_key'),
  path('password/reset/key/done/', allauth_views.PasswordResetFromKeyDoneView.as_view(), name='account_reset_password_from_key_done'),
  path('logout/',views.logout_view,name='logout'),
  path('profile/',views.profile,name='profile'),
  path('service/',views.services,name='services'),
  path('modify/',views.modify,name='modify'),
  path('service_detail/',views.service_detail,name='service_detail'),
  path('delete/',views.delete,name='delete'),
  path('services/', views.show_service, name='show_service'),
  path('services/load/', views.load_services, name='load_services'),
  path('search_filter/',views.search_filter,name='search_filter'),
  path('test/',views.test,name='test'),
  path('ds/<int:id>',views.describe_service,name='ds'),
  path('ContactArtisan/',views.ContactArtisan,name='ContactArtisan'),
  path('mark_as_done/',views.mark_as_done,name='mark_as_done'),
  path('dashboard/',views.dashboard,name='dashboard'),
  path('change_status/',views.change_status,name='change_status'),
  path('harasse/',views.harasse,name='harasse'),
]
