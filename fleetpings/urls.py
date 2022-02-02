"""
pages url config
"""

# Django
from django.urls import path

# AA Fleet Pings
from fleetpings import views

app_name: str = "fleetpings"

urlpatterns = [
    path("", views.index, name="index"),
    # ajax calls
    path("call/create-optimer/", views.ajax_create_optimer, name="ajax_create_optimer"),
    path(
        "call/create-srp-link/", views.ajax_create_srp_link, name="ajax_create_srp_link"
    ),
]
