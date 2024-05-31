import json
import logging
import datetime
from decimal import Decimal, getcontext
from typing import Any, List

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView, CreateView, View, TemplateView, ListView

from routes_management.forms import RouteCreateForm, StationOrderFormSet
from routes_management.models import Route
from stations.models import Station, StationOrder

logger = logging.getLogger("routes_management.views")


class RouteGenerateView(LoginRequiredMixin, View):
    form_class = RouteCreateForm
    template_name = "pages/routes/menu.html"

    def get(self, request, *args, **kwargs):
        context = {"form": self.form_class()}
        context["routes"] = Route.objects.all()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        logger.debug("RouteGenerateView post")

        stations = json.loads(request.POST["waypoints"])
        route_data = json.loads(request.POST["route_data"])
        driver_id = json.loads(request.POST["driver"])
        logger.debug(driver_id)
        driver = get_user_model().objects.filter(id=driver_id).first()

        route = Route.objects.create(
            date=None,
            duration=str(datetime.timedelta(seconds=route_data["duration"]["value"])),
            driver=driver,
        )
        route.save()
        for i, station_pk in enumerate(stations, 0):
            station = Station.objects.filter(pk=station_pk).first()
            station.route.add(route, through_defaults={"order": i})
            station.save()
        return JsonResponse({"status": "success"})


class RouteDetailView(LoginRequiredMixin, DetailView):
    model = Route
    template_name = "pages/routes/detail.html"


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


class RouteListView(LoginRequiredMixin, ListView):
    pass


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
