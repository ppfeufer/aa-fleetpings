"""
Form declarations
"""

# Django
from django import forms
from django.utils.translation import gettext_lazy as _

# AA Fleet Pings
from fleetpings.app_settings import timezones_installed
from fleetpings.models import FleetType

# from django.core.handlers.wsgi import WSGIRequest
# from django.db.models import Q


def _get_timezones_module_hint_text() -> str:
    if timezones_installed():
        return _(
            " Timezones module is installed. Link to time zone conversion will be "
            "added automatically if you set a date and time here."
        )

    return ""


# def _get_ping_targets(request: WSGIRequest):
#     def rectree(toplevel):
#         children_list_of_tuples = list()
#
#         if toplevel.children.active():
#             for child in toplevel.children.active():
#                 children_list_of_tuples.append(tuple((child.id, child.name)))
#
#         return children_list_of_tuples
#
#     data = list()
#     additional_discord_ping_targets = (
#         DiscordPingTargets.objects.filter(
#             Q(restricted_to_group__in=request.user.groups.all())
#             | Q(restricted_to_group__isnull=True),
#             is_enabled=True,
#         )
#         .distinct()
#         .order_by("name")
#     )
#
#     for toplevel in additional_discord_ping_targets:
#         childrens = rectree(toplevel)
#         data.append(tuple((toplevel.name, tuple(childrens))))
#
#     return tuple(data)


class FleetTypeAdminForm(forms.ModelForm):
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
            "embed_color": forms.TextInput(attrs={"type": "color"}),
        }


class FleetPingForm(forms.Form):
    """
    Fleet Ping Form
    """

    ping_target = forms.CharField(
        label=_("Ping Target"), widget=forms.Select(choices={})
    )
    pre_ping = forms.BooleanField(
        initial=False,
        required=False,
        label=_("Pre-Ping"),
        help_text=_("Mark this checkbox if this should be a pre-ping."),
    )
    ping_channel = forms.CharField(
        label=_("Ping To"),
        widget=forms.Select(choices={}),
        help_text=_("Select a channel to ping automatically"),
    )
    fleet_type = forms.CharField(
        label=_("Fleet Type"),
        widget=forms.Select(choices={}),
        help_text=_("Select a fleet type"),
    )
    fleet_commander = forms.CharField(
        required=True,
        label=_("FC Name"),
        max_length=254,
        widget=forms.TextInput(attrs={"placeholder": _("Who is the FC?")}),
    )
    fleet_name = forms.CharField(
        required=True,
        label=_("Fleet Name"),
        max_length=254,
        widget=forms.TextInput(
            attrs={"placeholder": _("What is the fleet name in fleet finder?")}
        ),
    )
    formup_location = forms.CharField(
        label=_("Formup Location"), widget=forms.Select(choices={})
    )
    formup_time = forms.CharField(
        required=True,
        label=_("Formup Time"),
        max_length=254,
        help_text=_(
            "To enable this field, either make it a Pre-Ping (checkbox above) or "
            "uncheck &quot;Formup NOW&quot; (checkbox below)."
        )
        + _get_timezones_module_hint_text(),
    )
    formup_now = forms.BooleanField(
        initial=True,
        required=False,
        label=_("Formup NOW"),
        help_text=_(
            "If this checkbox is active, formup time will be set to &quot;NOW&quot; "
            "and the time in the field above (if any is set) will be ignored."
        ),
    )
    fleet_comms = forms.CharField(
        label=_("Fleet Comms"), widget=forms.Select(choices={})
    )
    fleet_doctrine = forms.CharField(
        label=_("Doctrine"), widget=forms.Select(choices={})
    )
    srp = forms.BooleanField(
        initial=False,
        required=False,
        label=_("SRP"),
        help_text=_("Is this fleet covered by SRP?"),
    )
    srp_link = forms.BooleanField(
        initial=False,
        required=False,
        label=_("Create SRP Link"),
        help_text=_(
            "If this checkbox is active, a SRP link specific for this fleet will be "
            "created.<br>Leave blank if unsure."
        ),
    )
    additional_information = forms.CharField(
        required=False,
        label=_("Additional Information"),
        widget=forms.Textarea(
            attrs={
                "rows": 10,
                "cols": 20,
                "input_type": "textarea",
                "placeholder": _(
                    "Feel free to add some more information about the fleet ..."
                ),
            }
        ),
    )
    optimer = forms.BooleanField(
        initial=False,
        required=False,
        label=_("Create Optime"),
        help_text=_(
            "If this checkbox is active, a fleet operations timer for this pre-ping "
            "will be created."
        ),
    )
