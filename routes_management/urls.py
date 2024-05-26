from django.urls import path
from routes_management import views

urlpatterns = [
    path("stations/", views.StationsView.as_view(), name="stations"),
    path("stations/list", views.StationListView.as_view(), name="stations"),
    path('stations/create/', views.StationCreateView.as_view(), name='station-create'),
    path('stations/<int:station_id>/delete', views.StationDeleteView.as_view(), name='station-delete'),
]
