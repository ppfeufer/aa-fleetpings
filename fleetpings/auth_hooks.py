"""
Hook into AA
"""

# Alliance Auth
from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

# AA Fleet Pings
from fleetpings import __title_translated__, urls


class AaFleetpingsMenuItem(MenuItemHook):  # pylint: disable=too-few-public-methods
    """
    This class ensures only authorized users will see the menu entry
    """

    def __init__(self):
        """
        Constructor
        """

        # Setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            text=__title_translated__,
            classes="fa-regular fa-bell",
            url_name="fleetpings:index",
            navactive=["fleetpings:index"],
        )

    def render(self, request):
        """
        Render the menu item

        :param request:
        :type request:
        :return:
        :rtype:
        """

        return (
            MenuItemHook.render(self, request=request)
            if request.user.has_perm(perm="fleetpings.basic_access")
            else ""
        )


@hooks.register("menu_item_hook")
def register_menu():
    """
    Register our menu entry

    :return:
    :rtype:
    """

    return AaFleetpingsMenuItem()


@hooks.register("url_hook")
def register_urls():
    """
    Register our URLs

    :return:
    :rtype:
    """

    return UrlHook(urls=urls, namespace="fleetpings", base_url=r"^fleetpings/")
