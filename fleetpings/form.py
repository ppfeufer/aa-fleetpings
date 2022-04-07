"""
Form declarations
"""

# Django
from django import forms

# AA Fleet Pings
from fleetpings.models import FleetType

# from django.core.handlers.wsgi import WSGIRequest
# from django.db.models import Q


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

    ping_target = forms.CharField(label="Ping Target", widget=forms.Select(choices={}))
    # ping_target = forms.MultipleChoiceField(choices=_get_ping_targets(_user))
