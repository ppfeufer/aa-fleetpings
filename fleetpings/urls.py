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
        r"^call/create_optimer/$",
        views.ajax_create_optimer_on_preping,
        name="ajax_create_optimer",
    ),
]
