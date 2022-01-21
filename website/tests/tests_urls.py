from django.test import TestCase
from django.urls import resolve, reverse
from website.views import AboutView, HomeView


class TestWebsiteUrls(TestCase):
    """ Reverse an URL and resolve that URL to see which view Django calls.
        Check status code returned from responses.
    """

    # VIEWS

    def test_website_home_url_is_resolved(self):
        url = reverse('website_home')
        resolver_match = resolve(url)
        self.assertEquals(resolver_match.func.view_class, HomeView)

    def test_website_about_url_is_resolved(self):
        url = reverse('website_about')
        resolver_match = resolve(url)
        self.assertEquals(resolver_match.func.view_class, AboutView)

    # RESPONSES

    def test_website_home_url_response(self):
        """
            Successful code - 200.
        """
        response = self.client.get(reverse('website_home'))
        self.assertEqual(response.status_code, 200) 

    def test_website_about_url_response(self):
        """
            Successful code - 200.
        """
        response = self.client.get(reverse('website_about'))
        self.assertEqual(response.status_code, 200)