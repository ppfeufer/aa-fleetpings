"""
Managers for our models
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
        Return the value for given setting key
        :param setting_key:
        :return:
        """

        return getattr(self.first(), setting_key)

    def get_queryset(self):
        """
        Get a Setting queryset
        :return:
        """

        return SettingQuerySet(self.model)
