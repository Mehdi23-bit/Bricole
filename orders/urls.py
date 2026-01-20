from django.urls import path

from orders import views

urlpatterns = [
    path("ContactArtisan/", views.ContactArtisan, name="ContactArtisan"),
    path("mark_as_done/", views.mark_as_done, name="mark_as_done"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("change_status/", views.change_status, name="change_status"),
]
