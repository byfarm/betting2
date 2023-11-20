from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("nfl/", views.nfl, name="nfl"),
    path("ufc/", views.ufc, name="ufc"),
    path("nba/", views.nba, name="nba"),
]
