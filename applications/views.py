import logging
from typing import Any, List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, Q
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView

from applications.forms import ApplicationForm
from applications.models import Application

logger = logging.getLogger("routes_management.views")


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
        date_str = request.GET.get("date", None)
        part_of_day = request.GET.get("part_of_day", None)

        if date_str:
            try:
                selected_date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return JsonResponse({"error": "Invalid date format"}, status=400)
        else:
            selected_date = timezone.now().date()

        logger.debug(part_of_day)
        applications = Application.objects.filter(
            date=selected_date, route__isnull=True, part_of_day=part_of_day
        )

        logger.debug(applications)
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


class ApplicationDeleteView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        application: Application = Application.objects.get(pk=self.kwargs["pk"])
        application.delete()

        if self.request.user.is_superuser:
            return redirect("application-archive")
        return redirect("user-history")
