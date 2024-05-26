from msilib.schema import ListView

from django.shortcuts import render
from django.views.generic import DetailView, CreateView, View, TemplateView


class RouteListView(ListView):
    pass


class RouteDetailView(DetailView):
    pass


class RouteGenerateView(View):
    pass


class RouteApproveView(CreateView):
    pass


class RouteHistoryView(TemplateView):
    pass
