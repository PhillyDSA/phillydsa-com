# -*- coding: utf-8 -*-

"""Models for home page (root) of wagtail site."""

from __future__ import absolute_import, unicode_literals

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailsearch import index

from common.blocks import (
    CaptionImageBlock,
    BlockQuoteBlock,
    HeaderH1,
    Subhead)


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
    ])

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
