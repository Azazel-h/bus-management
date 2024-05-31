from django.contrib.auth import get_user_model
from django.forms import (
    ModelForm,
    BooleanField,
    modelformset_factory,
    IntegerField,
    TimeField,
)

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
    order = IntegerField(required=False, label="")
    passed = BooleanField(required=False, label="")
    passengers_taken = IntegerField(required=False, label="")
    passed_time = TimeField(required=False, label="")

    class Meta:
        model = StationOrder
        fields = ["order", "passed", "passed_time", "passengers_taken"]


StationOrderFormSet = modelformset_factory(StationOrder, form=StationOrderForm, extra=0)


class RouteForm(ModelForm):
    class Meta:
        model = Route
        fields = [
            "driver",
            "duration",
            "passengers_count",
            "price",
            "approved",
            "completed",
        ]
        labels = {
            "driver": "Водитель",
            "duration": "Продолжительность",
            "passengers_count": "Количество пассажиров",
            "price": "Цена",
            "approved": "Подтверждено",
            "completed": "Завершено",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["driver"].required = False
        self.fields["driver"].queryset = get_user_model().objects.filter(
            is_staff=True, is_superuser=False
        )
        self.fields["duration"].required = False
