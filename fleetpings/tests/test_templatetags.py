# Django
from django.template import Context, Template
from django.test import TestCase

# AA Fleet Pings
from fleetpings import __version__


class TestVersionedStatic(TestCase):
    """
    Test fleetpings_versioned_static template tage
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
