from django.shortcuts import render

import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, View

from stations.models import Station


class StationsView(TemplateView):
    template_name = "pages/stations/show.html"

    def get_context_data(self, **kwargs):
        context = super(StationsView, self).get_context_data(**kwargs)
        context["stations"] = Station.objects.all().order_by("name")
        return context


class StationListView(View):
    def get(self, request):
        stations = Station.objects.all()
        stations_list = [
            {
                "id": station.id,
                "name": station.name,
                "latitude": station.latitude,
                "longitude": station.longitude,
            }
            for station in stations
        ]
        return JsonResponse(stations_list, safe=False)


class StationCreateView(View):
    def post(self, request):
        data = json.loads(request.body)
        station = Station.objects.create(
            name=data["name"], latitude=data["latitude"], longitude=data["longitude"]
        )
        return JsonResponse(
            {
                "id": station.id,
                "name": station.name,
                "latitude": station.latitude,
                "longitude": station.longitude,
            }
        )


class StationDeleteView(View):
    def delete(self, request, station_id):
        station = get_object_or_404(Station, id=station_id)
        station.delete()
        return JsonResponse({"status": "success"})
