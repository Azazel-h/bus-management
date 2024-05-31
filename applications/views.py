from typing import Any, List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView

from applications.forms import ApplicationForm
from applications.models import Application


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = "pages/applications/add.html"
    success_url = reverse_lazy("user-history")

    def form_valid(self, form):
        form.instance.passenger = self.request.user
        return super().form_valid(form)


class ApplicationListView(View):
    def get(self, request):
        applications = Application.objects.filter(
            date__gte=timezone.now(), departure__route__isnull=True
        ).order_by("date")
        stations = []
        for application in applications:
            stations.append(
                {
                    "id": application.id,
                    "departure": application.departure.name,
                    "departure_id": application.departure.id,
                    "arrival": application.arrival.name,
                    "arrival_id": application.arrival.id,
                }
            )
        return JsonResponse(stations, safe=False)


class ApplicationArchiveListView(ListView):
    model = Application
    template_name = "pages/applications/archive.html"
    context_object_name = "applications"

    def get_queryset(self, *args: Any, **kwargs: Any) -> List[Application]:
        applications = Application.objects.filter().order_by("date")
        return applications
