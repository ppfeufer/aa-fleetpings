"""
Testing the template tags
"""

# Django
from django.conf import settings
from django.template import Context, Template

# AA Fleet Pings
from fleetpings.tests import BaseTestCase


class TestReverseUrl(BaseTestCase):
    """
    Test fleetpings_reverse_url template tag
    """

    def test_reverse_url(self):
        """
        Test should return a reversed URL

        :return:
        :rtype:
        """

        context = Context(dict_={"doctrine_pk": "1"})
        template_to_render = Template(
            template_string=(
                "{% load fleetpings %}"
                "{% fleetpings_reverse_url 'fittings:view_doctrine' doctrine_pk %}"
            )
        )

        rendered_template = template_to_render.render(context=context)

        self.assertInHTML(
            needle=f'{settings.SITE_URL}/fittings/doctrine/{context["doctrine_pk"]}/',
            haystack=rendered_template,
        )
