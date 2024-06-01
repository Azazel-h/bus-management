import json
import logging
import datetime
from decimal import Decimal, getcontext
from typing import Any, List

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    DetailView,
    CreateView,
    View,
    TemplateView,
    ListView,
    FormView,
)

from applications.models import Application
from routes_management.forms import RouteCreateForm, StationOrderFormSet, RouteForm
from routes_management.models import Route
from stations.models import Station, StationOrder

logger = logging.getLogger("routes_management.views")


class RouteGenerateView(LoginRequiredMixin, View):
    form_class = RouteCreateForm
    template_name = "pages/routes/menu.html"

    def get(self, request, *args, **kwargs):
        context = {"form": self.form_class()}
        context["routes"] = Route.objects.filter(completed=False)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        logger.debug(request.POST)

        stations = json.loads(request.POST["waypoints"])
        route_data = json.loads(request.POST["route_data"])
        applications = json.loads(request.POST["applications"])
        date_str = request.POST["date"]
        logger.debug(applications)
        try:
            # Парсим дату в формате 'YYYY-MM-DD'
            date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError as e:
            logger.error(f"Invalid date format: {e}")
            return JsonResponse({"error": "Invalid date format"}, status=400)
        application_ids = [app["id"] for app in applications]

        # Получение количества уникальных пассажиров
        unique_passenger_count = (
            Application.objects.filter(id__in=application_ids)
            .values("passenger")
            .distinct()
            .count()
        )
        logger.debug(unique_passenger_count)
        driver_id = json.loads(request.POST["driver"])
        logger.debug(driver_id)
        driver = get_user_model().objects.filter(id=driver_id).first()

        route = Route.objects.create(
            date=date,
            duration=str(datetime.timedelta(seconds=route_data["duration"]["value"])),
            driver=driver,
            passengers_count=unique_passenger_count,
            price=(route_data["distance"]["value"] / 1000 * 100)
            / unique_passenger_count,
            distance=route_data["distance"]["value"],
        )
        route.save()
        for application in applications:
            application_obj = Application.objects.filter(pk=application["id"]).first()
            application_obj.route = route
            application_obj.save()

        for i, station_pk in enumerate(stations, 1):
            station = Station.objects.filter(pk=station_pk).first()
            station.route.add(route, through_defaults={"order": i})
            station.save()
        return JsonResponse({"status": "success"})


class RouteDetailView(LoginRequiredMixin, DetailView):
    model = Route
    template_name = "pages/routes/detail.html"


class RouteUpdateView(FormView):
    template_name = "pages/routes/update.html"
    form_class = RouteForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        route_id = self.kwargs["pk"]
        route = get_object_or_404(Route, pk=route_id)

        if self.request.POST:
            context["form"] = RouteForm(self.request.POST, instance=route)
            context["formset"] = StationOrderFormSet(
                self.request.POST, queryset=route.stationorder_set.all()
            )
        else:
            context["form"] = RouteForm(instance=route)
            context["formset"] = StationOrderFormSet(
                queryset=route.stationorder_set.all()
            )

        return context

    def form_valid(self, form):
        route_id = self.kwargs["pk"]
        route = get_object_or_404(Route, pk=route_id)
        logger.debug(form.cleaned_data)
        route.update(commit=True, **form.cleaned_data)

        station_orders = StationOrder.objects.filter(route=route).order_by("order")
        formset = StationOrderFormSet(self.request.POST, queryset=station_orders)
        if formset.is_valid():
            for form in formset:
                station_order = form.instance
                form_data = form.cleaned_data
                form_data["id"] = station_order.id
                if form_data["passed"] and form_data["passed_time"] is None:
                    form_data["passed_time"] = timezone.now()
                elif not form_data["passed"]:
                    form_data["passed_time"] = None
                station_order.update(commit=True, **form_data)

        return super().form_valid(form)

    def get_queryset(self):
        route_id = self.kwargs["pk"]
        return StationOrder.objects.filter(pk=route_id)

    def get_success_url(self):
        return reverse_lazy("route-detail", kwargs={"pk": self.kwargs["pk"]})


class RouteApproveView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        route: Route = Route.objects.get(pk=self.kwargs["pk"])
        route.approved = True
        route.save()
        return redirect("route-menu")


class RouteEndView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        route: Route = Route.objects.get(pk=self.kwargs["pk"])
        route.completed = True
        route.save()

        return redirect("route-history")


class RouteDeleteView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        route: Route = Route.objects.get(pk=self.kwargs["pk"])
        route.delete()
        return redirect("route-menu")


class RouteHistoryView(LoginRequiredMixin, ListView):
    model = Route
    template_name = "pages/routes/history.html"
    context_object_name = "routes"

    def get_queryset(self, *args: Any, **kwargs: Any) -> List[Route]:
        routes = Route.objects.filter(completed=True, approved=True).order_by("date")
        return routes


class RouteTrackingView(LoginRequiredMixin, View):
    template_name = "pages/routes/tracking.html"

    def get(self, request, pk):
        route = get_object_or_404(Route, id=pk)
        station_orders = StationOrder.objects.filter(route=route).order_by("order")
        formset = StationOrderFormSet(queryset=station_orders)
        return render(request, self.template_name, {"formset": formset, "route": route})

    def post(self, request, pk):
        route = get_object_or_404(Route, id=pk)
        station_orders = StationOrder.objects.filter(route=route).order_by("order")
        formset = StationOrderFormSet(request.POST, queryset=station_orders)

        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                if instance.passed and instance.passed_time is None:
                    instance.passed_time = timezone.now()
                elif not instance.passed:
                    instance.passed_time = None
                instance.save()
        return redirect("route-tracking", pk=pk)
