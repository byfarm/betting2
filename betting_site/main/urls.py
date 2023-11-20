from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("nfl/", views.nfl, name="v1"),
    path("ufc/", views.ufc, name="v1"),
]
