#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import calendar
import datetime
from dateutil import relativedelta

from django.db import models
from django.shortcuts import render
from django.utils.text import slugify

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel)
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.blocks import ImageChooserBlock


def make_calendar(year=datetime.datetime.now().year, month=datetime.datetime.now().month):
    """Return curr year & month & list of lists representing days in curr month."""
    calendar.setfirstweekday(calendar.SUNDAY)
    year, month = int(year), int(month)
    return year, month, calendar.monthcalendar(year, month)


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
                              .filter(membercalendarevent__event_date__day=day).order_by('membercalendarevent__event_date')
        elif month:
            events = events_qs.filter(membercalendarevent__event_date__year=year)\
                              .filter(membercalendarevent__event_date__month=month).order_by('membercalendarevent__event_date')
        elif year:
            events = events_qs.filter(membercalendarevent__event_date__year=year).order_by('membercalendarevent__event_date')
        else:
            events = events_qs.filter(membercalendarevent__event_date__month=datetime.datetime.now().month).order_by('membercalendarevent__event_date')

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
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
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

    @property
    def iso_start_time(self):
        """Return ISO-formatted start time for event."""
        return datetime.datetime(
            self.event_date.year,
            self.event_date.month,
            self.event_date.day,
            self.event_start_time.hour,
            self.event_start_time.minute).isoformat()

    @property
    def iso_end_time(self):
        """Return ISO-formatted end time for event."""
        return datetime.datetime(
            self.event_date.year,
            self.event_date.month,
            self.event_date.day,
            self.event_end_time.hour,
            self.event_end_time.minute).isoformat()

    def save(self, *args, **kwargs):
        """Override to have a more specific slug w/ date & title."""
        self.slug = "{0}-{1}".format(self.event_date.strftime("%Y-%m-%d"), slugify(self.title))
        super().save(*args, **kwargs)
