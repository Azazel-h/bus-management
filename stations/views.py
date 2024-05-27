from django.shortcuts import render

import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View

from stations.models import Station


class StationsView(TemplateView):
    template_name = "pages/stations/show.html"


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
    @method_decorator(csrf_exempt)
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
    @method_decorator(csrf_exempt)
    def delete(self, request, station_id):
        station = get_object_or_404(Station, id=station_id)
        station.delete()
        return JsonResponse({"status": "success"})
