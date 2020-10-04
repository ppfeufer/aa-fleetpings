# -*- coding: utf-8 -*-

"""
pages url config
"""

from django.urls import path

from fleetpings import views


app_name: str = "fleetpings"

urlpatterns = [
    path("", views.index, name="index"),
]
