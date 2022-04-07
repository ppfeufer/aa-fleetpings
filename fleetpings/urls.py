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
    path("ajax/create-optimer/", views.ajax_create_optimer, name="ajax_create_optimer"),
    path(
        "ajax/create-srp-link/", views.ajax_create_srp_link, name="ajax_create_srp_link"
    ),
]
