from django.urls import path

from reviews import views

urlpatterns = [
    path("harasse/", views.harasse, name="harasse"),
    path("comment/", views.comment, name="comment"),
]
