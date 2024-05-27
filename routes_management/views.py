from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, CreateView, View, TemplateView, ListView


class RouteListView(LoginRequiredMixin, ListView):
    pass


class RouteDetailView(LoginRequiredMixin, DetailView):
    pass


class RouteGenerateView(LoginRequiredMixin, View):
    template_name = "pages/routes/add.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class RouteApproveView(LoginRequiredMixin, CreateView):
    pass


class RouteHistoryView(LoginRequiredMixin, TemplateView):
    pass
