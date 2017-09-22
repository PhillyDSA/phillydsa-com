#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from bs4 import BeautifulSoup as bs

from django.test import TestCase
from django.test import Client

from wagtail.wagtailcore.models import Page

from member_calendar.models import MemberCalendarEvent
from member_calendar.utils import make_calendar


class MemberCalendarTests(TestCase):
    """Tests for MemberCalendar app."""

    fixtures = ['member_calendar/test_fixtures/new_data.json']

    def setUp(self):
        """Common code to run before every test."""
        self.client = Client()

    def test_member_calendar_event_ical_creation(self):
        """Test that events properly export to ical format."""
        event = MemberCalendarEvent.objects.all().first()

        ics = str(event.to_ical())
        assert 'BEGIN:VCALENDAR' in ics
        assert 'SUMMARY:Test event' in ics, ics

        req = self.client.get(event.url + '?format=ical')
        assert req.status_code == 200, req.status_code
        assert req._headers['content-type'] == ('Content-Type', 'text/calendar')

        req = self.client.get(event.url)
        assert req.status_code == 200, req.status_code
        assert req._headers['content-type'] == ('Content-Type', 'text/html; charset=utf-8')

        req = self.client.get(event.url + '?format=test')
        assert req.content.decode('utf8') == 'Could not export event\n\nUnrecognised format.'

    def test_member_calendar_home_page(self):
        """Test routing and MemberCalendarHomePage rendering."""
        req = self.client.get('/calendar/')
        assert req.status_code == 200, req.status_code
        assert isinstance(req.context['month'], int)

        req = self.client.get('/calendar/2017/8/')
        assert req.status_code == 200, req.status_code
        assert req.context['events_dict'].get(1).title == 'Test event'

        req = self.client.get('/calendar/2014/1/')
        assert len(req.context['events_dict']) == 0

        req = self.client.get('/calendar/2017/8/1/')
        assert len(req.context['events']) == 1
        assert req.context['events'][0].title == 'Test event'

    def test_correct_template_rendering_month_page(self):
        """Test to ensure that templates render correctly for the month."""
        req = self.client.get('/calendar/2017/8/')
        soup = bs(req.content, 'html.parser')
        links = soup.find_all('a')

        assert req.status_code == 200, req.status_code
        assert any(['/calendar/2017/8/1/' in link['href'] for link in links]), links
        assert '- Events for August 2017' in soup.title.string, soup.title.string

    def test_correct_template_rendering_day_page(self):
        """Test to ensure that template renders correctly for the day."""
        req = self.client.get('/calendar/2017/8/1/')
        soup = bs(req.content, 'html.parser')
        links = soup.find_all('a')

        assert req.status_code == 200, req.status_code
        assert '- Events for August 1, 2017' in soup.title.string, soup.title.string
        assert any(["Test event" in link.text for link in links]), links

    def test_make_calendar(self):
        """Test function to create a list of lists calendar."""
        year, month, cal = make_calendar(year=2017, month=5)
        assert year == 2017
        assert month == 5
        assert isinstance(cal, list)
        assert isinstance(cal[0], list)

    def test_event_creation(self):
        """Test creating events and slug/location properties."""
        homepage = Page.objects.get(url_path='/')
        mce = MemberCalendarEvent()
        mce.title = 'Test event'
        mce.event_date = datetime.date(2017, 1, 1)
        mce.event_end_time = datetime.time(12, 0)
        mce.event_start_time = datetime.time(13, 0)
        homepage.add_child(instance=mce)
        mce.save()

        assert mce.slug == '2017-01-01-test-event'
        assert mce.event_location == "To be determined"

        mce.location_name = 'Test location'
        mce.location_street_address = '123 Main Street'
        mce.location_city = 'Anywhere'
        mce.location_state = 'PA'
        mce.location_zip_code = '19107'

        mce.save()
        assert mce.event_location == "123 Main Street, Anywhere, PA 19107", mce.event_location
