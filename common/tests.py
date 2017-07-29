#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt

from django.test import TestCase

from common.templatetags import common_tags as tags
from bulletins.models import BulletinEmail


class FilterTests(TestCase):
    """Tests for common/common_tags."""

    def test_zulu_time_filter(self):
        """Test conversion to zulu time."""
        date_obj = dt.date(2017, 1, 1)
        zulu_string = tags.zulu_time(date_obj)
        assert zulu_string == "20170101T050000Z", zulu_string

    def test_generate_page_title(self):
        """Test deriving a <title> tag from a Page."""
        with open('common/test_data/bulletins.bulletinemail.json') as f:
            page = BulletinEmail.from_json(f.read(), check_fks=False)
            title = tags.generate_page_title(page)
            assert title == 'None - Show up to Resist Trump, Resist Corporate Greed, and Support Workers!', title

    def test_generate_page_description(self):
        """Test deriving a <meta description> tag from a page."""
        with open('common/test_data/bulletins.bulletinemail.json') as f:
            page = BulletinEmail.from_json(f.read(), check_fks=False)
            desc = tags.generate_page_description(page)
            assert desc == 'SEIU 32BJ Philadelphia Airport workers need your support on July 13. PHL Airport workers-who are mostly low-wage immigrants and people ...', desc
