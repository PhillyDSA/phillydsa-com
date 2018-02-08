# -*- coding: utf-8 -*-
from django.test import TestCase

import datetime

from django.test import Client
from blog.models import BlogEntry


class BlogTests(TestCase):
    """Tests for Blog Entriesl and associated views."""

    fixtures = ['blog/test_fixtures/new_data.json']

    def setUp(self):
        """Set up for each test method to run."""
        self.client = Client()

    def test_blog__model(self):
        """Test creation of Blog Entries."""
        blog_entry = BlogEntry.objects.all().first()
        assert blog_entry.title == "blog entry 1", blog_entry.title
        assert blog_entry.blog_date == datetime.date(2017, 11, 1)
        blog_entry.title = 'Test'
        blog_entry.save()
        assert blog_entry.title == 'Test'

    def test_blog_home_page(self):
        """Test routing and MemberCalendarHomePage rendering."""
        req = self.client.get('/blog/')
        assert req.status_code == 200
        # should be three entries with test db
        # each entry in resources is a blog page
        # test consists of 3 entries:
        # (1) title: blog entry 1, author: author 1, date: 11/1/17, tags: tag1, tag2
        # (2) title: blog entry 2, author: author 2, date: 11/1/17, tags: tag1, tag3
        # (3) title: blog entry 3, author: author 1, date: 11/2/17, tags: tag1
        blog_entries = req.context['resources']
        assert len(blog_entries) == 3
        # in reverse order
        assert blog_entries[0].title == "blog entry 3", blog_entries[0].title

        # when the functionality is put in for display by month/year or author,
        # will have tests here for that

    def test_blog_home_page_empty(self):
        """Test empty page (no blog entries)."""
        req = self.client.get('/news/?page=100')
        assert req.status_code == 200, req.status_code

    def test_tags(self):
        """Test routing and MemberCalendarHomePage rendering."""
        req = self.client.get('/tags/?tag=tag1')
        assert req.status_code == 200
        blog_entries = req.context['blogpages']
        assert len(blog_entries) == 3

        req = self.client.get('/tags/?tag=tag2')
        assert req.status_code == 200
        blog_entries = req.context['blogpages']
        assert len(blog_entries) == 1

        req = self.client.get('/tags/?tag=tag3')
        assert req.status_code == 200
        blog_entries = req.context['blogpages']
        assert len(blog_entries) == 1

        req = self.client.get('/tags/?tag=tag4')
        assert req.status_code == 200
        blog_entries = req.context['blogpages']
        assert len(blog_entries) == 0
