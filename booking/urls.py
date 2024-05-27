from django.urls import path

from booking import views

urlpatterns = [
    path("add/", views.ApplicationCreateView.as_view(), name="booking-add"),
    path("list/", views.ApplicationListView.as_view(), name="booking-list"),
]
