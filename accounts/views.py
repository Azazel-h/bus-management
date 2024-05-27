from typing import Any, List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView
from accounts.forms import CustomUserCreateForm
import logging

from booking.models import Application

logger = logging.getLogger("accounts.views")


class SignUpView(CreateView):
    form_class = CustomUserCreateForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class UserHistoryView(LoginRequiredMixin, ListView):
    model = Application
    success_url = reverse_lazy("user-history")
    template_name = "pages/user/history.html"
    context_object_name = "applications"

    def get_queryset(self, *args: Any, **kwargs: Any) -> QuerySet:
        applications: QuerySet = Application.objects.filter(passenger=self.request.user)
        return applications
