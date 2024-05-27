from django.urls import path
from routes_management import views

urlpatterns = [
    path("", views.RouteGenerateView.as_view(), name="route-add"),
]
