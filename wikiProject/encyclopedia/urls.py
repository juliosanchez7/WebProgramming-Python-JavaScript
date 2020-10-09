from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.TITLE, name="TITLE"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("create/newpage", views.newpage, name="newpage"),
    path("random/page", views.randompage, name="randompage")
]


