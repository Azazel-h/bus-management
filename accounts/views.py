from typing import Any, List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView
from accounts.forms import CustomUserCreateForm
import logging

from applications.models import Application
from routes_management.models import Route

logger = logging.getLogger("accounts.views")


class SignUpView(CreateView):
    form_class = CustomUserCreateForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class UserHistoryView(LoginRequiredMixin, ListView):
    model = Application
    template_name = "pages/user/history.html"
    context_object_name = "applications"

    def get_queryset(self, *args: Any, **kwargs: Any) -> QuerySet:
        applications: QuerySet = Application.objects.filter(
            passenger=self.request.user
        ).order_by("date")
        return applications


class CurrentDriverRoutesView(LoginRequiredMixin, ListView):
    model = Route
    template_name = "pages/user/driver_tracking.html"
    context_object_name = "routes"

    def get_queryset(self, *args: Any, **kwargs: Any):
        current_routes = Route.objects.filter(
            driver=self.request.user, approved=True, completed=False
        ).order_by("-date")
        return current_routes


class UpcomingDriverRouteListView(LoginRequiredMixin, ListView):
    model = Route
    template_name = "pages/user/driver_upcoming.html"
    context_object_name = "routes"

    def get_queryset(self, *args: Any, **kwargs: Any) -> List[Route]:
        routes = Route.objects.filter(
            driver=self.request.user, approved=False, completed=False
        ).order_by("-date")
        logger.debug(routes)
        return routes


class DriverRouteHistoryView(LoginRequiredMixin, ListView):
    model = Route
    template_name = "pages/user/driver_history.html"
    context_object_name = "routes"

    def get_queryset(self, *args: Any, **kwargs: Any) -> List[Route]:
        routes = Route.objects.filter(
            driver=self.request.user, completed=True, approved=True
        ).order_by("-date")
        return routes
