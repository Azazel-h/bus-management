from django.contrib.auth import get_user_model
from django.forms import ModelForm, BooleanField, modelformset_factory

from routes_management.models import Route
from stations.models import StationOrder


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
        self.fields["driver"].queryset = get_user_model().objects.filter(
            is_staff=True, is_superuser=False
        )


class StationOrderForm(ModelForm):
    passed = BooleanField(required=False, label="")

    class Meta:
        model = StationOrder
        fields = ["passed"]


StationOrderFormSet = modelformset_factory(StationOrder, form=StationOrderForm, extra=0)
