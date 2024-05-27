from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, View, TemplateView, ListView


class RouteListView(LoginRequiredMixin, ListView):
    pass


class RouteDetailView(LoginRequiredMixin, DetailView):
    pass


class RouteGenerateView(LoginRequiredMixin, View):
    pass


class RouteApproveView(LoginRequiredMixin, CreateView):
    pass


class RouteHistoryView(LoginRequiredMixin, TemplateView):
    pass
