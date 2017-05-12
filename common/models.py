# -*- coding: utf-8 -*-

"""Models for home page (root) of wagtail site."""

from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from common.snippets import FundraisingSnippet

from common.blocks import (
    CaptionImageBlock,
    BlockQuoteBlock,
    HeaderH1,
    Subhead,
    CallToAction
)


class TopLevelPage(Page):
    """Render a top-level page.

    Useful for things like FAQ/About Us/etc.
    """

    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', CaptionImageBlock()),
        ('h1', HeaderH1(classname="full title")),
        ('subhead', Subhead(classname="full title")),
        ('block_quote', BlockQuoteBlock()),
        ('call_to_action', CallToAction()),
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
