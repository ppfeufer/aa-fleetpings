# -*- coding: utf-8 -*-

"""
pages url config
"""

from django.conf.urls import url

from fleetpings import views


app_name: str = "fleetpings"

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(
        r"^create_optimer/$",
        views.create_optimer_on_preping,
        name="create_optimer",
    ),
]
