#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import calendar
from datetime import datetime

from django.db import models
from django.template.response import TemplateResponse

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


def make_calendar():
    """Return curr year & month & list of lists representing days in curr month."""
    year, month = datetime.now().year, datetime.now().month
    calendar.setfirstweekday(calendar.SUNDAY)
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
        elif kwargs.get('year'):
            template_name = 'member_calendar/events_by_year.html'
        else:
            template_name = 'member_calendar/member_calendar_home_page.html'

        return TemplateResponse(
            request,
            template_name,
            self.get_context(request, *args, **kwargs)
        )

    def get_context(self, request, *args, **kwargs):
        """Return context and order by event date rather than pub date."""
        context = super(MemberCalendarHomePage, self).get_context(request)
        events_qs = self.get_children().live()
        if kwargs.get('day'):
            events = events_qs.filter(membercalendarevent__event_date__year=kwargs.get('year'))\
                              .filter(membercalendarevent__event_date__month=kwargs.get('month'))\
                              .filter(membercalendarevent__event_date__day=kwargs.get('day')).order_by('membercalendarevent__event_date')
        elif kwargs.get('month'):
            events = events_qs.filter(membercalendarevent__event_date__year=kwargs.get('year'))\
                              .filter(membercalendarevent__event_date__month=kwargs.get('month')).order_by('membercalendarevent__event_date')
        elif kwargs.get('year'):
            events = events_qs.filter(membercalendarevent__event_date__year=kwargs.get('year')).order_by('membercalendarevent__event_date')
        else:
            events = events_qs.order_by('membercalendarevent__event_date')
        current_year, current_month, cal = make_calendar()

        events_dict = {}
        [events_dict.update({ev.specific.event_date.day: ev}) for ev in events]
        context = {
            'events': events,
            'events_dict': events_dict,
            'calendar': cal,
            'month_name': calendar.month_name[current_month],
            'month': current_month,
            'year': current_year,
            'extra_data': kwargs,
        }
        print(context)
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

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('event_date'),
        FieldPanel('event_start_time'),
        FieldPanel('event_end_time'),
        StreamFieldPanel('body'),
    ]

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('seo_title'),
            FieldPanel('show_in_menus'),
            FieldPanel('search_description'),
        ])]

    def save(self, *args, **kwargs):
        """Override to have a more specific slug w/ date & title."""
        self.slug = "{0}-{1}".format(self.event_date.strftime("%Y-%m-%d"), slugify(self.title))
        super().save(*args, **kwargs)
