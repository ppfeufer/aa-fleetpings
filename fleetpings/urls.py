"""
pages url config
"""

# Django
from django.conf.urls import url

# AA Fleet Pings
from fleetpings import views

app_name: str = "fleetpings"

urlpatterns = [
    url(r"^$", views.index, name="index"),
    # ajax calls
    url(
        r"^call/create-optimer/$",
        views.ajax_create_optimer,
        name="ajax_create_optimer",
    ),
    url(
        r"^call/create-srp-link/$",
        views.ajax_create_srp_link,
        name="ajax_create_srp_link",
    ),
]
