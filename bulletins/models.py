#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import calendar
import datetime

from django.db import models
from django.shortcuts import render
from django.utils.text import slugify

from dateutil import relativedelta

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel)
from wagtail.wagtailsearch import index

from member_calendar.utils import make_calendar
from common.blocks import STRUCT_BLOCKS


class BulletinHomePage(RoutablePageMixin, Page):
    """Page to display all email bulletins."""

    subpage_types = ['EmailBulletin']

    @route(r'^$')
    @route(r'^(?P<year>[0-9]{4})/$')
    @route(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$')
    @route(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/$')
    def bulletins(self, request, *args, **kwargs):
        """Return current month bulletins or archives by kwarg."""
        if kwargs.get('day'):
            template_name = 'member_calendar/bulletins_by_day.html'
        elif kwargs.get('month'):
            template_name = 'member_calendar/bulletins_by_month.html'
        elif kwargs.get('year'):
            template_name = 'member_calendar/bulletins_by_year.html'
        else:
            template_name = 'member_calendar/bulletins_by_month.html'

        return render(
            request,
            template_name,
            self.get_context(request, *args, **kwargs)
        )

    def get_context(self, request, *args, **kwargs):
        """Return context and order by event date rather than pub date."""
        context = super(BulletinHomePage, self).get_context(request)
        bulletins_qs = self.get_children().live()
        day, month, year = (kwargs.get('day', None),
                            kwargs.get('month', None),
                            kwargs.get('year', None))
        if day:
            bulletins = bulletins_qs.filter(bulletinemail__bulletin_date__year=year)\
                              .filter(bulletinemail__bulletin_date__month=month)\
                              .filter(bulletinemail__bulletin_date__day=day)\
                              .order_by('membercalendarevent__event_date')
        elif month:
            bulletins = bulletins_qs.filter(bulletinemail__bulletin_date__year=year)\
                              .filter(bulletinemail__bulletin_date__month=month)\
                              .order_by('membercalendarevent__event_date')
        elif year:
            bulletins = bulletins_qs.filter(bulletinemail__bulletin_date__year=year)\
                              .order_by('membercalendarevent__event_date')
        else:
            bulletins = bulletins_qs.filter(bulletinemail__bulletin_date__month=datetime.datetime.now().month)\
                              .order_by('membercalendarevent__event_date')

        year, month, cal = make_calendar(year=year or datetime.datetime.now().year,
                                         month=month or datetime.datetime.now().month)

        bulletin_dict = {}
        [bulletin_dict.update({bulletin.specific.bulletin_date.day: bulletin}) for bulletin in bulletins]
        next_month = datetime.date(year, month, 1) + relativedelta.relativedelta(months=1)
        previous_month = datetime.date(year, month, 1) + relativedelta.relativedelta(months=-1)
        context = {
            'calendar': cal,
            'bulletins': bulletins,
            'bulletin_dict': bulletin_dict,
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


class BulletinEmail(Page):
    """Page for a single bulletin email."""

    bulletin_date = models.DateField("Bulletin Date")

    body = StreamField(STRUCT_BLOCKS)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
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
        self.slug = "{0}-{1}".format(self.bulletin_date.strftime("%Y-%m-%d"), slugify(self.title))
        super().save(*args, **kwargs)
