"""
Form declarations
"""

# Django
from django import forms
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

# AA Fleet Pings
from fleetpings.models import FleetType, Setting


def _get_discord_markdown_hint_text() -> str:
    """
    Get the formatted help text for any field that allows Discord Markdown
    :return:
    """

    discord_helpdesk_url = (
        "https://support.discord.com/hc/en-us/articles/210298617"
        "-Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline- "
    )

    discord_markdown_link_text = _("Discord Markdown")
    discord_markdown_link = (
        f'<a href="{discord_helpdesk_url}" target="_blank" rel="noopener noreferer">'
        f"{discord_markdown_link_text}</a>"
    )

    return format_lazy(
        _("Hint: You can use {discord_markdown_link} to format the text."),
        discord_markdown_link=discord_markdown_link,
    )


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
        widgets = {"embed_color": forms.TextInput(attrs={"type": "color"})}


class SettingAdminForm(forms.ModelForm):
    """
    Form definitions for the FleetType form in admin
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta
        """

        model = Setting
        fields = "__all__"
        widgets = {"default_embed_color": forms.TextInput(attrs={"type": "color"})}


class FleetPingForm(forms.Form):
    """
    Fleet Ping Form
    """

    ping_target = forms.CharField(
        required=False,
        label=_("Ping Target"),
        widget=forms.Select(choices={}),
        help_text=_("Who do you want to ping?"),
    )
    pre_ping = forms.BooleanField(
        initial=False,
        required=False,
        label=_("Pre-Ping"),
        help_text=_("Mark this checkbox if this should be a pre-ping."),
    )
    ping_channel = forms.CharField(
        required=False,
        label=_("Ping To"),
        widget=forms.Select(choices={}),
        help_text=_("Select a channel to ping automatically."),
    )
    fleet_type = forms.CharField(
        required=False, label=_("Fleet Type"), widget=forms.Select(choices={})
    )
    fleet_commander = forms.CharField(
        required=False,
        label=_("FC Name"),
        max_length=254,
        widget=forms.TextInput(attrs={"placeholder": _("Who is the FC?")}),
    )
    fleet_name = forms.CharField(
        required=False,
        label=_("Fleet Name"),
        max_length=254,
        widget=forms.TextInput(
            attrs={"placeholder": _("What is the fleet name in fleet finder?")}
        ),
    )
    formup_location = forms.CharField(
        required=False,
        label=_("Formup Location"),
        widget=forms.TextInput(
            attrs={"list": "formupLocationList", "class": "flexdatalist"}
        ),
    )
    formup_time = forms.CharField(
        required=False,
        label=_("Formup Time"),
        max_length=254,
        widget=forms.TextInput(attrs={"disabled": "disabled", "autocomplete": "off"}),
        help_text=_(
            "To enable this field, either make it a Pre-Ping (checkbox above) or "
            "uncheck &quot;Formup NOW&quot; (checkbox below)."
        ),
    )
    formup_timestamp = forms.CharField(
        required=False,
        label=_("Formup Timestamp"),
        widget=forms.TextInput(attrs={"hidden": "hidden"}),
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
        required=False,
        label=_("Fleet Comms"),
        widget=forms.TextInput(
            attrs={"list": "fleetCommsList", "class": "flexdatalist"}
        ),
    )
    fleet_doctrine = forms.CharField(
        required=False,
        label=_("Doctrine"),
        widget=forms.TextInput(
            attrs={"list": "fleetDoctrineList", "class": "flexdatalist"}
        ),
    )
    fleet_doctrine_url = forms.CharField(
        required=False,
        label=_("Doctrine link"),
        widget=forms.TextInput(attrs={"hidden": "hidden"}),
    )
    webhook_embed_color = forms.CharField(
        required=False,
        label=_("Webhook Embed Color"),
        widget=forms.TextInput(attrs={"hidden": "hidden"}),
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
                    "Feel free to add some more information about the fleet …"
                ),
            }
        ),
        help_text=_get_discord_markdown_hint_text(),
    )
    optimer = forms.BooleanField(
        initial=False,
        required=False,
        label=_("Create Optimer"),
        help_text=_(
            "If this checkbox is active, a fleet operations timer for this pre-ping "
            "will be created."
        ),
    )
