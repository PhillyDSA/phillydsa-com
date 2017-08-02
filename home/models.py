# -*- coding: utf-8 -*-

"""Models for home page (root) of wagtail site."""

from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailcore import blocks

from common import blocks as common_blocks
from common.snippets import FundraisingSnippet
from common.open_graph import OpenGraphMixin


class HomePage(OpenGraphMixin, Page):
    """Controls rendering of PhillyDSA home page.

    This is the first page that you see hosted at /
    """

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

    fundraising_snippet = models.ForeignKey(
        FundraisingSnippet,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        SnippetChooserPanel('fundraising_snippet')
    ]
