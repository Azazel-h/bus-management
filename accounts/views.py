from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import CustomUserCreateForm
import logging

logger = logging.getLogger("accounts.views")


class SignUpView(CreateView):
    form_class = CustomUserCreateForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"