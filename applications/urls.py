from django.urls import path

from applications import views

urlpatterns = [
    path("add/", views.ApplicationCreateView.as_view(), name="application-add"),
    path("list/", views.ApplicationListView.as_view(), name="application-list"),
    path(
        "archive/",
        views.ApplicationArchiveListView.as_view(),
        name="application-archive",
    ),
]
