from django.contrib.auth import get_user_model
from django.forms import ModelForm

from routes_management.models import Route


class RouteCreateForm(ModelForm):
    """
    Форма для создания парковки.
    """

    class Meta:
        model = Route
        fields = ("driver",)
        labels = {"driver": "Водитель"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["driver"].queryset = (
            get_user_model()
            .objects.filter(is_staff=True, is_superuser=False)
            .exclude(route__isnull=False)
        )
