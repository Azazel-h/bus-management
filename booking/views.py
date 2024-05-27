from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView

from booking.forms import ApplicationForm
from booking.models import Application


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'pages/booking/add.html'
    success_url = reverse_lazy('user-history')

    def form_valid(self, form):
        form.instance.passenger = self.request.user
        return super().form_valid(form)

