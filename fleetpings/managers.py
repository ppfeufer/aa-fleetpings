"""
Managers for the fleetpings app
"""

# Django
from django.db import models


class SettingQuerySet(models.QuerySet):
    """
    SettingQuerySet
    """

    def delete(self):
        """
        Delete action

        Override:   We don't allow deletion here, so we make sure the object
                    is saved again and not deleted
        :return:
        """

        return super().update()


class SettingManager(models.Manager):
    """
    SettingManager
    """

    def get_setting(self, setting_key: str) -> str:
        """
        Get a setting

        :param setting_key:
        :type setting_key:
        :return:
        :rtype:
        """

        return getattr(self.first(), setting_key)

    def get_queryset(self):
        """
        Get the queryset

        :return:
        :rtype:
        """

        return SettingQuerySet(self.model)
