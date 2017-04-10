# -*- coding: utf-8 -*-
from django.db import models

from django.utils.text import slugify
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel)
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.blocks import ImageChooserBlock


class MemberCalendarHomePage(Page):
    """Page to display all events."""

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full')
    ]

    def get_context(self, request):
        """Order by event date rather than pub date."""
        context = super(MemberCalendarHomePage, self).get_context(request)
        events = self.get_children().live().order_by('membercalendarevent__event_date')
        context['events'] = events
        return context


class MemberCalendarEvent(Page):
    """Page for a single event."""

    event_date = models.DateTimeField("Event Date")
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
