from django.urls import path

from accounts import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("history/", views.UserHistoryView.as_view(), name="user-history"),
    path(
        "current-routes/", views.CurrentDriverRoutesView.as_view(), name="driver-routes"
    ),
    path(
        "upcoming-routes/",
        views.UpcomingDriverRouteListView.as_view(),
        name="upcoming-routes",
    ),
    path(
        "routes-history/",
        views.DriverRouteHistoryView.as_view(),
        name="history-routes",
    ),
]
