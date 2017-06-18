#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import calendar
import datetime

from django.db import models
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.text import slugify

from icalendar import Event, Calendar
from dateutil import relativedelta

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel)
from wagtail.wagtailsearch import index

from member_calendar.utils import make_calendar
from common import blocks as common_blocks


class MemberCalendarHomePage(RoutablePageMixin, Page):
    """Page to display all events."""

    subpage_types = ['MemberCalendarEvent']
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full')
    ]

    @route(r'^$')
    @route(r'^(?P<year>[0-9]{4})/$')
    @route(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$')
    @route(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/$')
    def events(self, request, *args, **kwargs):
        """Return current month events or archives by kwarg."""
        if kwargs.get('day'):
            template_name = 'member_calendar/events_by_day.html'
        elif kwargs.get('month'):
            template_name = 'member_calendar/events_by_month.html'
        elif kwargs.get('year'):
            template_name = 'member_calendar/events_by_year.html'
        else:
            template_name = 'member_calendar/events_by_month.html'

        return render(
            request,
            template_name,
            self.get_context(request, *args, **kwargs)
        )

    def get_context(self, request, *args, **kwargs):
        """Return context and order by event date rather than pub date."""
        context = super(MemberCalendarHomePage, self).get_context(request)
        events_qs = self.get_children().live()
        day, month, year = (kwargs.get('day', None),
                            kwargs.get('month', None),
                            kwargs.get('year', None))
        if day:
            events = events_qs.filter(membercalendarevent__event_date__year=year)\
                              .filter(membercalendarevent__event_date__month=month)\
                              .filter(membercalendarevent__event_date__day=day)\
                              .order_by('membercalendarevent__event_date')
        elif month:
            events = events_qs.filter(membercalendarevent__event_date__year=year)\
                              .filter(membercalendarevent__event_date__month=month)\
                              .order_by('membercalendarevent__event_date')
        elif year:
            events = events_qs.filter(membercalendarevent__event_date__year=year)\
                              .order_by('membercalendarevent__event_date')
        else:
            events = events_qs.filter(membercalendarevent__event_date__month=datetime.datetime.now().month)\
                              .order_by('membercalendarevent__event_date')

        year, month, cal = make_calendar(year=year or datetime.datetime.now().year,
                                         month=month or datetime.datetime.now().month)

        events_dict = {}
        [events_dict.update({ev.specific.event_date.day: ev}) for ev in events]
        next_month = datetime.date(year, month, 1) + relativedelta.relativedelta(months=1)
        previous_month = datetime.date(year, month, 1) + relativedelta.relativedelta(months=-1)
        context = {
            'calendar': cal,
            'events': events,
            'events_dict': events_dict,
            'extra_data': kwargs,
            'month': month,
            'month_name': calendar.month_name[month],
            'next_month': next_month.month,
            'next_year': next_month.year,
            'previous_month': previous_month.month,
            'previous_year': previous_month.year,
            'page': self,
            'year': year,
        }
        return context


class MemberCalendarEvent(Page):
    """Page for a single event."""

    event_date = models.DateField("Event Date")
    event_start_time = models.TimeField("Start time")
    event_end_time = models.TimeField("End time")
    body = StreamField([
        ('banner_image', common_blocks.BannerImage()),
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', common_blocks.CaptionImageBlock()),
        ('h1', common_blocks.HeaderH1(classname="full title")),
        ('subhead', common_blocks.Subhead(classname="full title")),
        ('block_quote', common_blocks.BlockQuote()),
        ('call_to_action', common_blocks.CallToAction()),
        ('small_call_to_action', common_blocks.CTAButton()),
    ])

    location_street_address = models.CharField(max_length=255, blank=True)
    location_city = models.CharField(max_length=255, blank=True)
    location_zip_code = models.CharField(max_length=5, blank=True)
    location_state = models.CharField(max_length=100, blank=True)
    location_name = models.CharField(max_length=500, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('event_date'),
        FieldPanel('event_start_time'),
        FieldPanel('event_end_time'),
        FieldPanel('location_name'),
        FieldPanel('location_street_address'),
        FieldPanel('location_city'),
        FieldPanel('location_state'),
        FieldPanel('location_zip_code'),
        StreamFieldPanel('body'),
    ]

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('seo_title'),
            FieldPanel('show_in_menus'),
            FieldPanel('search_description'),
        ])]

    def serve(self, request):
        """Serve request based on options in GET method to add ical attachment."""
        if "format" in request.GET:
            if request.GET['format'] == 'ical':
                # Export to ical format
                response = HttpResponse(self.to_ical(), content_type='text/calendar')
                response['Content-Disposition'] = 'attachment; filename=' + self.slug + '.ics'
                return response
            else:
                # Unrecognised format error
                message = 'Could not export event\n\nUnrecognised format.'
                return HttpResponse(message, content_type='text/plain')
        else:
            # Display event page as usual
            return super().serve(request)

    def event_datetime(self, ev_date=None, ev_time=None):
        """Return a combined datetime.datetime object for the event."""
        return datetime.datetime(ev_date.year, ev_date.month, ev_date.day,
                                 ev_time.hour, ev_time.minute)

    @property
    def event_start_dt(self):
        """Return event start time as a datetime.datetime obj."""
        return self.event_datetime(ev_date=self.event_date, ev_time=self.event_start_time)

    @property
    def event_end_dt(self):
        """Return event end time as a datetime.datetime obj."""
        return self.event_datetime(ev_date=self.event_date, ev_time=self.event_end_time)

    @property
    def iso_start_time(self):
        """Return ISO-formatted start time for event."""
        return self.event_start_dt.isoformat()

    @property
    def iso_end_time(self):
        """Return ISO-formatted end time for event."""
        return self.event_end_dt.isoformat()

    def save(self, *args, **kwargs):
        """Override to have a more specific slug w/ date & title."""
        self.slug = "{0}-{1}".format(self.event_date.strftime("%Y-%m-%d"), slugify(self.title))
        super().save(*args, **kwargs)

    @property
    def event_location(self):
        """Return an event location or "To be determined"."""
        if not all([self.location_street_address, self.location_city, self.location_state, self.location_zip_code]):
            return "To be determined"
        else:
            return ", ".join([self.location_street_address,
                              self.location_city,
                              self.location_state]) + self.location_zip_code

    def to_ical(self):
        """Return an iCal compatible file representing the event."""
        cal = Calendar()
        event = Event()

        event.add('summary', self.title)
        event.add('uid', '{0}@phillydsa.com'.format(self.slug))
        event.add('dtstart', self.event_datetime(self.event_date, self.event_start_time))
        event.add('dtend', self.event_datetime(self.event_date, self.event_end_time))
        event.add('location', ','.join([self.location_street_address,
                                        self.location_city,
                                        self.location_state,
                                        self.location_zip_code]))
        event.add('organizer', 'PhillyDSA')
        cal.add_component(event)
        return cal.to_ical()
