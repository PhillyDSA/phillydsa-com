# -*- coding: utf-8 -*-

"""Common structblocks for use in editor."""

from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock


class BlockQuoteBlock(blocks.StructBlock):
    """Create a block quote StructBlock element."""

    quote = blocks.TextBlock(required=True, max_length=255, classname="full")

    class Meta:
        """Implement class specific attrs here."""

        icon = 'openquote'
        template = 'common/_block_quote.html'


class CaptionImageBlock(blocks.StructBlock):
    """Create an image with caption and optional alignment."""

    photo = ImageChooserBlock()
    photo_alignment = blocks.ChoiceBlock(choices=(
        ('left', 'Left'),
        ('right', 'Right'),
        ('center', 'Center'))
    )
    caption = blocks.CharBlock(max_length=255)
    caption_alignment = blocks.ChoiceBlock(choices=(
        ('tl', 'Left'),
        ('tr', 'Right'),
        ('tc', 'Center'))
    )

    class Meta:
        """Class specific attrbutes."""

        icon = 'image'
        template = 'common/_captioned_image_block.html'


class HeaderH1(blocks.CharBlock):
    """Create an H1 header."""

    class Meta:
        """Class specific attributes."""

        icon = 'title'
        template = 'common/_h1.html'


class Subhead(blocks.CharBlock):
    """Create a subhead for use within page."""

    class Meta:
        """Class specific attributes."""

        icon = 'title'
        template = 'common/_subhead.html'


class CallToAction(blocks.StructBlock):
    """Create a call to action for use within page."""

    title = blocks.CharBlock(max_length=255)
    cta_copy = blocks.CharBlock(max_length=255)
    button_title = blocks.CharBlock(max_length=255)
    button_link = blocks.PageChooserBlock(required=False)
    button_external_link = blocks.URLBlock(required=False)

    class Meta:
        """Class specific attributes."""

        icon = 'title'
        template = 'common/_cta.html'
