"""
Testing the template tags
"""

# Django
from django.template import Context, Template
from django.test import TestCase, override_settings

# Alliance Auth (External Libs)
from app_utils.urls import site_absolute_url

# AA Fleet Pings
from fleetpings import __version__
from fleetpings.constants import PACKAGE_NAME
from fleetpings.helper.static_files import calculate_integrity_hash


class TestVersionedStatic(TestCase):
    """
    Test the `fleetpings_static` template tag
    """

    @override_settings(DEBUG=False)
    def test_versioned_static(self):
        """
        Test should return the versioned static

        :return:
        :rtype:
        """

        context = Context(dict_={"version": __version__})
        template_to_render = Template(
            template_string=(
                "{% load fleetpings %}"
                "{% fleetpings_static 'css/fleetpings.min.css' %}"
                "{% fleetpings_static 'js/fleetpings.min.js' 'module' %}"
            )
        )

        rendered_template = template_to_render.render(context=context)

        expected_static_css_src = (
            f'/static/{PACKAGE_NAME}/css/fleetpings.min.css?v={context["version"]}'
        )
        expected_static_css_src_integrity = calculate_integrity_hash(
            "css/fleetpings.min.css"
        )
        expected_static_js_src = (
            f'/static/{PACKAGE_NAME}/js/fleetpings.min.js?v={context["version"]}'
        )
        expected_static_js_src_integrity = calculate_integrity_hash(
            "js/fleetpings.min.js"
        )

        self.assertIn(member=expected_static_css_src, container=rendered_template)
        self.assertIn(
            member=expected_static_css_src_integrity, container=rendered_template
        )
        self.assertIn(member=expected_static_js_src, container=rendered_template)
        self.assertIn(
            member=expected_static_js_src_integrity, container=rendered_template
        )

    @override_settings(DEBUG=True)
    def test_versioned_static_with_debug_enabled(self) -> None:
        """
        Test versioned static template tag with DEBUG enabled

        :return:
        :rtype:
        """

        context = Context({"version": __version__})
        template_to_render = Template(
            template_string=(
                "{% load fleetpings %}"
                "{% fleetpings_static 'css/fleetpings.min.css' %}"
            )
        )

        rendered_template = template_to_render.render(context=context)

        expected_static_css_src = (
            f'/static/{PACKAGE_NAME}/css/fleetpings.min.css?v={context["version"]}'
        )

        self.assertIn(member=expected_static_css_src, container=rendered_template)
        self.assertNotIn(member="integrity=", container=rendered_template)

    @override_settings(DEBUG=False)
    def test_invalid_file_type(self) -> None:
        """
        Test should raise a ValueError for an invalid file type

        :return:
        :rtype:
        """

        context = Context({"version": __version__})
        template_to_render = Template(
            template_string=(
                "{% load fleetpings %}" "{% fleetpings_static 'invalid/invalid.txt' %}"
            )
        )

        with self.assertRaises(ValueError):
            template_to_render.render(context=context)


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
