"""
Hook into AA
"""

# Alliance Auth
from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

# AA Fleet Pings
from fleetpings import __title__, urls


class AaFleetpingsMenuItem(MenuItemHook):  # pylint: disable=too-few-public-methods
    """
    This class ensures only authorized users will see the menu entry
    """

    def __init__(self):
        # Setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            __title__,
            "far fa-bell fa-fw",
            "fleetpings:index",
            navactive=["fleetpings:index"],
        )

    def render(self, request):
        """
        Check if the user has the permission to view this app
        :param request:
        :return:
        """

        if request.user.has_perm("fleetpings.basic_access"):
            return MenuItemHook.render(self, request)

        return ""


@hooks.register("menu_item_hook")
def register_menu():
    """
    Register our menu item
    :return:
    """

    return AaFleetpingsMenuItem()


@hooks.register("url_hook")
def register_urls():
    """
    Register our base url
    :return:
    """

    return UrlHook(urls, "fleetpings", r"^fleetpings/")
