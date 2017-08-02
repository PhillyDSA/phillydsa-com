# -*- coding: utf-8 -*-
import datetime

from django.test import TestCase
from django.test import Client
from bulletins.models import BulletinEmail


class BulletinsTests(TestCase):
    """Tests for Bulletin Email and associated views."""

    fixtures = ['bulletins/test_fixtures/new_data.json']

    def setUp(self):
        """Set up for each test method to run."""
        self.client = Client()

    def test_bulletin_html_creation(self):
        """Test that bulletins properly export to html for actionnetwork."""
        bulletin = BulletinEmail.objects.all().first()

        req = self.client.get(bulletin.url + '?format=email')
        assert req.status_code == 200
        assert req._headers['content-type'] == ('Content-Type', 'text/plain; charset="UTF8"')

        req = self.client.get(bulletin.url)
        assert req.status_code == 200
        assert req._headers['content-type'] == ('Content-Type', 'text/html; charset=utf-8')

        req = self.client.get(bulletin.url + '?format=test')
        assert req.content.decode('utf8') == 'Could not export bulletin\n\nUnrecognised format.'

    def test_bulletin__model(self):
        """Test creation of Bulletins."""
        bulletin = BulletinEmail.objects.all().first()
        assert bulletin.title == "Test Bulletin", bulletin.title
        assert bulletin.bulletin_date == datetime.date(2017, 8, 1)
        bulletin.title = 'Test'
        bulletin.save()
        assert bulletin.title == 'Test'

    def test_bulletins_home_page(self):
        """Test routing and MemberCalendarHomePage rendering."""
        req = self.client.get('/news/')

        assert req.status_code == 200

        req = self.client.get('/news/2017/8/')
        bulletins = req.context['bulletins']
        assert len(bulletins) == 1
        assert bulletins[0].title == "Test Bulletin"
