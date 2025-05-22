"""
Testing the template tags
"""

# Django
from django.template import Context, Template
from django.test import TestCase

# Alliance Auth (External Libs)
from app_utils.urls import site_absolute_url


class TestReverseUrl(TestCase):
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
        site_url = site_absolute_url()

        self.assertInHTML(
            needle=f'{site_url}/fittings/doctrine/{context["doctrine_pk"]}/',
            haystack=rendered_template,
        )
