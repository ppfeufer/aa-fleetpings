"""
Form declarations
"""

# Django
from django.forms import ModelForm, TextInput

# AA Fleet Pings
from fleetpings.models import FleetType


class FleetTypeAdminForm(ModelForm):
    """
    Form definitions for the FleetType form in admin
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta
        """

        model = FleetType
        fields = "__all__"
        widgets = {
            "embed_color": TextInput(attrs={"type": "color"}),
        }
