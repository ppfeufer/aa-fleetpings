"""
Testing the template tags
"""

# Django
from django.template import Context, Template
from django.test import TestCase

# Alliance Auth (External Libs)
from app_utils.urls import site_absolute_url

# AA Fleet Pings
from fleetpings import __version__


class TestVersionedStatic(TestCase):
    """
    Test fleetpings_versioned_static template tag
    """

    def test_versioned_static(self):
        """
        Test should return versioned static
        :return:
        """

        context = Context({"version": __version__})
        template_to_render = Template(
            "{% load fleetpings_versioned_static %}"
            "{% fleetpings_static 'fleetpings/css/fleetpings.min.css' %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertInHTML(
            f'/static/fleetpings/css/fleetpings.min.css?v={context["version"]}',
            rendered_template,
        )


class TestReverseUrl(TestCase):
    """
    Test fleetpings_reverse_url template tag
    """

    def test_reverse_url(self):
        """
        Test should return a URL
        :return:
        """

        context = Context({"doctrine_pk": "1"})
        template_to_render = Template(
            "{% load fleetpings_urls %}"
            "{% fleetpings_reverse_url 'fittings:view_doctrine' doctrine_pk %}"
        )

        rendered_template = template_to_render.render(context)
        site_url = site_absolute_url()

        # self.assertEqual(rendered_template, 0)

        self.assertInHTML(
            f'{site_url}/fittings/doctrine/{context["doctrine_pk"]}/',
            rendered_template,
        )
