#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import calendar
import datetime
import logging

import premailer
from django.conf import settings
from django.db import models
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.text import slugify

from dateutil import relativedelta

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel)
from wagtail.wagtailsearch import index

from member_calendar.utils import make_calendar
from common import blocks as common_blocks


class BulletinHomePage(RoutablePageMixin, Page):
    """Page to display all email bulletins."""

    subpage_types = ['BulletinEmail']

    @route(r'^$')
    @route(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$')
    def bulletins(self, request, *args, **kwargs):
        """Return current month bulletins or archives by kwarg."""
        template_name = 'bulletins/bulletins_by_month.html'
        return render(request, template_name, self.get_context(request, *args, **kwargs))

    def get_context(self, request, *args, **kwargs):
        """Return context and order by event date rather than pub date."""
        context = super(BulletinHomePage, self).get_context(request)
        bulletins_qs = self.get_children().live()
        month, year = (kwargs.get('month', None),
                       kwargs.get('year', None))
        if month:
            bulletins = bulletins_qs.filter(bulletinemail__bulletin_date__year=year)\
                                    .filter(bulletinemail__bulletin_date__month=month)\
                                    .order_by('-bulletinemail__bulletin_date')
        else:
            bulletins = bulletins_qs.filter(bulletinemail__bulletin_date__month=datetime.datetime.now().month)\
                                    .order_by('-bulletinemail__bulletin_date')

        year, month, cal = make_calendar(year=year or datetime.datetime.now().year,
                                         month=month or datetime.datetime.now().month)

        next_month = datetime.date(year, month, 1) + relativedelta.relativedelta(months=1)
        previous_month = datetime.date(year, month, 1) + relativedelta.relativedelta(months=-1)
        context = {
            'calendar': cal,
            'bulletins': bulletins,
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

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('bulletin_date'),
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

    def to_email(self, *args, **kwargs):
        """Export a bulletin as an HTML file for emailing."""
        request = kwargs.get('request', None)
        template_string = render_to_string("bulletins/bulletin_html_email.html", self.get_context(request))
        prepared_resp = premailer.Premailer(template_string,
                                            base_url=settings.BASE_URL,
                                            remove_classes=True,
                                            strip_important=True,
                                            cssutils_logging_level=logging.CRITICAL).transform()
        return prepared_resp

    def serve(self, request):
        """Serve request based on options in GET method to add email."""
        if "format" in request.GET:
            if request.GET['format'] == 'email':
                # Export to plaint text email format
                response = HttpResponse(self.to_email(request=request), content_type='text/plain; charset="UTF8"')
                return response
            else:
                # Unrecognised format error
                message = 'Could not export bulletin\n\nUnrecognised format.'
                return HttpResponse(message, content_type='text/plain')
        else:
            # Display event page as usual
            return super().serve(request)
