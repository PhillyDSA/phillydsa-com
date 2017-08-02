# -*- coding: utf-8 -*-
from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

OG_TYPE_CHOICES = (
    ('article', 'Article'),
    ('website', 'Website'),
    ('book', 'Book'),
    ('video', 'Video'),
    ('profile', 'Profile'),
)


class OpenGraphMixin(models.Model):
    """Add open graph fields to Pages."""

    og_type = models.CharField(
        blank=False,
        default='website',
        max_length=127,
        choices=OG_TYPE_CHOICES,
        verbose_name='OG Page Type',
        help_text='See Object Types: https://developers.facebook.com/docs/reference/opengraph/',
    )
    share_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Share Image',
        help_text='Should be larger than 1200 x 630px\n See https://developers.facebook.com/docs/sharing/best-practices#images'
    )

    promote_panels = [
        Page.promote_panels[0],
        MultiFieldPanel(heading="Open Graph Configuration",
                        children=[
                            FieldPanel('og_type'),
                            ImageChooserPanel('share_image')])
    ]

    class Meta:
        """Class-specific attrs."""

        abstract = True
