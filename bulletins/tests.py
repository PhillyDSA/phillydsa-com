# -*- coding: utf-8 -*-
import datetime

from django.test import TestCase
from django.test import Client
from bulletins.models import BulletinEmail

FIXTURE_FILE = 'test_data/data-2017-06-30-22-06-35.json'


class BulletinsTests(TestCase):
    """Tests for Bulletin Email and associated views."""

    fixtures = [FIXTURE_FILE]

    def test_bulletin_html_creation(self):
        """Test that bulletins properly export to html for actionnetwork."""
        bull = BulletinEmail.objects.all().first()

        c = Client()
        req = c.get(bull.url + '?format=email')
        assert req.status_code == 200
        assert req._headers['content-type'] == ('Content-Type', 'text/plain; charset="UTF8"')

        req = c.get(bull.url)
        assert req.status_code == 200
        assert req._headers['content-type'] == ('Content-Type', 'text/html; charset=utf-8')

        req = c.get(bull.url + '?format=test')
        assert req.content.decode('utf8') == 'Could not export bulletin\n\nUnrecognised format.'

    def test_bulletin__model(self):
        """Test creation of Bulletins."""
        bull = BulletinEmail.objects.all().first()
        assert bull.title == "It's Convention Time!", bull.title
        assert bull.bulletin_date == datetime.date(2017, 6, 5)
        bull.title = 'Test'
        bull.save()
        assert bull.title == 'Test'

    def test_bulletins_home_page(self):
        """Test routing and MemberCalendarHomePage rendering."""
        c = Client()
        req = c.get('/news/')

        assert req.status_code == 200
        assert isinstance(req.context['month'], int)

        req = c.get('/news/2017/6/')
        bulletins = req.context['bulletins']
        assert len(bulletins) == 3
        assert bulletins[2].title == "It's Convention Time!"
