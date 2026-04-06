from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("analysis/", views.analysis, name="analysis"),
    path("add_observation/", views.add_observation, name="add_observation"),
    path("participants/", views.participants, name="participants"),
]