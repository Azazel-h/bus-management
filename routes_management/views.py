import json
import logging
from decimal import Decimal, getcontext

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView, CreateView, View, TemplateView, ListView

from routes_management.forms import RouteCreateForm
from routes_management.models import Route
from stations.models import Station

logger = logging.getLogger("routes_management.views")


class RouteListView(LoginRequiredMixin, ListView):
    pass


class RouteDetailView(LoginRequiredMixin, DetailView):
    pass


class RouteGenerateView(LoginRequiredMixin, View):
    form_class = RouteCreateForm
    template_name = "pages/routes/add.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request, *args, **kwargs):
        logger.debug("RouteGenerateView post")
        logger.debug(request.POST)

        stations = json.loads(request.POST["waypoints"])
        route_data = json.loads(request.POST["route_data"])
        driver = (
            get_user_model()
            .objects.filter(id=json.loads(request.POST["driver"]))
            .first()
        )
        for i, station_pk in enumerate(stations, 0):
            station = Station.objects.filter(pk=station_pk).first()
            # logger.debug(station.name)
            route = Route.objects.create(
                date=timezone.now(),
                arrival_time=timezone.now()
                + timezone.timedelta(seconds=route_data["duration"]["value"]),
                driver=driver,
            )
            route.save()
            station.route.add(route, through_defaults={"order": i})
            station.save()
        return JsonResponse({"status": "success"})


class RouteApproveView(LoginRequiredMixin, CreateView):
    pass


class RouteHistoryView(LoginRequiredMixin, TemplateView):
    pass
