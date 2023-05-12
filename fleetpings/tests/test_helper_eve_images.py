"""
Tests for the eve_images helper
"""

# Django
from django.test import TestCase

# Alliance Auth (External Libs)
from app_utils.testing import create_fake_user

# AA Fleet Pings
from fleetpings.helper.eve_images import get_character_portrait_from_evecharacter


class TestHelperEveImages(TestCase):
    """
    Test eve_images helper
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up groups and users
        """

        super().setUpClass()

        cls.user_1001 = create_fake_user(1001, "Peter Parker")

    def test_should_return_character_portrait_url(self):
        """
        Test should return character portrait URL
        :return:
        """

        character = self.user_1001.profile.main_character

        portrait_url = get_character_portrait_from_evecharacter(character=character)
        expected_url = f"https://images.evetech.net/characters/{character.character_id}/portrait?size=32"  # pylint: disable=line-too-long

        self.assertEqual(portrait_url, expected_url)

    def test_should_return_character_portrait_html(self):
        """
        Test should return character portrait HTML image tag
        :return:
        """

        character = self.user_1001.profile.main_character

        portrait_html = get_character_portrait_from_evecharacter(
            character=character, as_html=True
        )
        expected_url = f"https://images.evetech.net/characters/{character.character_id}/portrait?size=32"  # pylint: disable=line-too-long
        expected_html = (
            '<img class="aa-fleetpings-character-portrait img-rounded" '
            f'src="{expected_url}" alt="{character.character_name}" '
            'width="32" height="32">'
        )

        self.assertEqual(portrait_html, expected_html)
