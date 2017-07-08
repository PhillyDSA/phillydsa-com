#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test import Client

from member_calendar.models import MemberCalendarEvent
from member_calendar.utils import make_calendar

FIXTURE_FILE = 'member_calendar/test_fixtures/data.json'


class MemberCalendarTests(TestCase):
    """Tests for MemberCalendar app."""

    fixtures = [FIXTURE_FILE]

    def test_member_calendar_event_ical_creation(self):
        """Test that events properly export to ical format."""
        event = MemberCalendarEvent.objects.all().first()
        ics = str(event.to_ical())
        assert 'BEGIN:VCALENDAR' in ics
        assert 'SUMMARY:ABCs of Socialism Reading Group - May Session' in ics

        c = Client()
        req = c.get(event.url + '?format=ical')
        assert req.status_code == 200
        assert req._headers['content-type'] == ('Content-Type', 'text/calendar')

        req = c.get(event.url)
        assert req.status_code == 200
        assert req._headers['content-type'] == ('Content-Type', 'text/html; charset=utf-8')

        req = c.get(event.url + '?format=test')
        assert req.content.decode('utf8') == 'Could not export event\n\nUnrecognised format.'

    def test_member_calendar_model(self):
        """Test creation of MemberCalendarEvents."""
        event = MemberCalendarEvent.objects.all().first()
        assert event.title == 'ABCs of Socialism Reading Group - May Session'
        assert event.slug == '2017-05-21-abcs-of-socialism-reading-group-may-session'
        assert event.iso_start_time == '2017-05-21T10:00:00'
        assert event.iso_end_time == '2017-05-21T13:00:00'
        event.title = 'Test'
        event.save()
        assert event.title == 'Test'
        assert event.slug == '2017-05-21-test'

    def test_member_calendar_home_page(self):
        """Test routing and MemberCalendarHomePage rendering."""
        c = Client()
        req = c.get('/member-calendar/')

        assert req.status_code == 200
        assert isinstance(req.context['month'], int)

        req = c.get('/member-calendar/2017/5/')
        assert req.context['events_dict'].get(21).title == 'ABCs of Socialism Reading Group - May Session'

        req = c.get('/member-calendar/2014/1/')
        assert len(req.context['events_dict']) == 0

        req = c.get('/member-calendar/2017/5/21/')
        assert len(req.context['events']) == 1
        assert req.context['events'][0].title == 'ABCs of Socialism Reading Group - May Session'

    def test_correct_template_rendering_month_page(self):
        """Test to ensure that templates render correctly for the month."""
        c = Client()
        req = c.get('/member-calendar/2017/5/')

        assert "/member-calendar/2017/5/21" in req.content.decode('utf8')

    def test_correct_template_rendering_day_page(self):
        """Test to ensure that template renders correctly for the day."""
        c = Client()
        req = c.get('/member-calendar/2017/5/21/')

        assert "ABCs of Socialism Reading Group - May Session" in req.content.decode('utf8')

    def test_make_calendar(self):
        """Test function to create a list of lists calendar."""
        year, month, cal = make_calendar(year=2017, month=5)
        assert year == 2017
        assert month == 5
        assert isinstance(cal, list)
        assert isinstance(cal[0], list)
