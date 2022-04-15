"""
Pages url config
"""

# Django
from django.urls import path

# AA Fleet Pings
from fleetpings import views

app_name: str = "fleetpings"

urlpatterns = [
    path("", views.index, name="index"),
    # Ajax calls
    path(
        "ajax/create-fleet-ping/",
        views.ajax_create_fleet_ping,
        name="ajax_create_fleet_ping",
    ),
    path(
        "ajax/get-ping-targets-for-user/",
        views.ajax_get_ping_targets,
        name="ajax_get_ping_targets",
    ),
    path(
        "ajax/get-webhooks-for-user/",
        views.ajax_get_webhooks,
        name="ajax_get_webhooks",
    ),
    path(
        "ajax/get-fleet-types-for-user/",
        views.ajax_get_fleet_types,
        name="ajax_get_fleet_types",
    ),
    path(
        "ajax/get-formup-locations/",
        views.ajax_get_formup_locations,
        name="ajax_get_formup_locations",
    ),
    path(
        "ajax/get-fleet-comms/",
        views.ajax_get_fleet_comms,
        name="ajax_get_fleet_comms",
    ),
    path(
        "ajax/get-fleet-doctrines-for-user/",
        views.ajax_get_fleet_doctrines,
        name="ajax_get_fleet_doctrines",
    ),
]
