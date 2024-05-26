from django.contrib import admin
from django.urls import path, include

from core import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("routes/", include("routes_management.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]
