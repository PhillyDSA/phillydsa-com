#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt
import json

from django.test import TestCase, Client
from bs4 import BeautifulSoup as bs

from common.templatetags import common_tags as tags
from bulletins.models import BulletinEmail


class FilterTests(TestCase):
    """Tests for common/common_tags."""

    fixtures = ['common/test_fixtures/new_data.json']

    def test_zulu_time_filter(self):
        """Test conversion to zulu time."""
        date_obj = dt.date(2017, 1, 1)
        zulu_string = tags.zulu_time(date_obj)
        assert zulu_string == "20170101T050000Z", zulu_string

        date_obj = dt.datetime(2017, 1, 1, 0, 0)
        zulu_string = tags.zulu_time(date_obj)
        assert zulu_string == "20170101T050000Z", zulu_string

    def test_generate_page_title(self):
        """Test deriving a <title> tag from a Page."""
        with open('common/test_data/bulletins.bulletinemail.json') as f:
            page = BulletinEmail.from_json(f.read(), check_fks=False)
            title = tags.generate_page_title(page)
            assert title == 'Test Site - Show up to Resist Trump, Resist Corporate Greed, and Support Workers!', title

        # Check to make sure that we don't throw an error for page not found
        assert tags.generate_page_title(None) == ''

    def test_generate_page_description(self):
        """Test deriving a <meta description> tag from a page."""
        with open('common/test_data/bulletins.bulletinemail.json') as f:
            page = BulletinEmail.from_json(f.read(), check_fks=False)
            desc = tags.generate_page_description(page)
            assert desc == 'SEIU 32BJ Philadelphia Airport workers need your support on July 13. PHL Airport workers-who are mostly low-wage immigrants and people ...', desc

    def test_organziation_jsonld(self):
        """Test rendering of organization JSON+LD."""
        client = Client()
        req = client.get('/')

        soup = bs(req.content, 'html.parser')
        org_json = json.loads(soup.find('script', {'id': 'orgjson'}).get_text())

        assert org_json['name'] == 'Test Site'
        assert org_json['url'] == 'http://localhost'
        assert org_json['sameAs'] == ['https://www.facebook.com/example', 'https://www.twitter.com/example', 'https://instagram.com/example', 'https://youtube.com/example']
        assert org_json['address']['addressStreet'] == '123 Main Street', org_json['address']
