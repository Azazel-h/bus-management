from django.urls import path
from routes_management import views

urlpatterns = [
    path("", views.RouteGenerateView.as_view(), name="route-menu"),
    path("history/", views.RouteHistoryView.as_view(), name="route-history"),
    path("<int:pk>/approve/", views.RouteApproveView.as_view(), name="route-approve"),
    path("<int:pk>/delete/", views.RouteDeleteView.as_view(), name="route-delete"),
    path("<int:pk>/detail/", views.RouteDetailView.as_view(), name="route-detail"),
    path("<int:pk>/end/", views.RouteEndView.as_view(), name="route-end"),
    path(
        "<int:pk>/tracking/", views.RouteTrackingView.as_view(), name="route-tracking"
    ),
]
