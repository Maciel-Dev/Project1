from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="wiki"),
    path("search", views.search, name="search"),
    path("newPage", views.newPage, name="newPage"),
    path("pageEdit/<str:namePage>", views.pageEdit, name="pageEdit"),
    path("randomPage", views.randomPage, name="randomPage")
]
