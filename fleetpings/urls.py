"""
URL configuration for fleetpings app
"""

# Django
from django.urls import include, path

# AA Fleet Pings
from fleetpings import views

app_name: str = "fleetpings"

urlpatterns = [
    path(route="", view=views.index, name="index"),
    # Ajax calls
    path(
        route="ajax/",
        view=include(
            [
                path(
                    route="create-fleet-ping/",
                    view=views.ajax_create_fleet_ping,
                    name="ajax_create_fleet_ping",
                ),
                path(
                    route="get-ping-targets-for-user/",
                    view=views.ajax_get_ping_targets,
                    name="ajax_get_ping_targets",
                ),
                path(
                    route="get-webhooks-for-user/",
                    view=views.ajax_get_webhooks,
                    name="ajax_get_webhooks",
                ),
                path(
                    route="get-fleet-types-for-user/",
                    view=views.ajax_get_fleet_types,
                    name="ajax_get_fleet_types",
                ),
                path(
                    route="get-formup-locations/",
                    view=views.ajax_get_formup_locations,
                    name="ajax_get_formup_locations",
                ),
                path(
                    route="get-fleet-comms/",
                    view=views.ajax_get_fleet_comms,
                    name="ajax_get_fleet_comms",
                ),
                path(
                    route="get-fleet-doctrines-for-user/",
                    view=views.ajax_get_fleet_doctrines,
                    name="ajax_get_fleet_doctrines",
                ),
            ]
        ),
    ),
]
