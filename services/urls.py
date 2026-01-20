from django.urls import path

from services import views

app_name='services'

urlpatterns = [
    path("home/", views.home, name="home"),
    path("profile/", views.profile, name="profile"),
    path("service/", views.services, name="services"),
    path("modify/", views.modify, name="modify"),
    path("service_detail/", views.service_detail, name="service_detail"),
    path("delete/", views.delete, name="delete"),
    path("services/", views.show_service, name="show_service"),
    path("services/load/", views.load_services, name="load_services"),
    path("search_filter/", views.search_filter, name="search_filter"),
    path("test/", views.test, name="test"),
    path("ds/<int:id>", views.describe_service, name="ds"),
    path("deleteService/", views.deleteService, name="deleteService"),
    path("modifyService/", views.modifyService, name="modifyService"),
]
