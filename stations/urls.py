from django.urls import path
from stations import views

urlpatterns = [
    path("", views.StationsView.as_view(), name="stations"),
    path("list/", views.StationListView.as_view(), name="stations-list"),
    path('create/', views.StationCreateView.as_view(), name='station-create'),
    path('<int:station_id>/delete/', views.StationDeleteView.as_view(), name='station-delete'),
]
