# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.shortcuts import render
from django.utils.text import slugify

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase


from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel, MultiFieldPanel
from wagtail.wagtailsearch import index

from common import blocks as common_blocks
from common.open_graph import OpenGraphMixin


class BlogHomePage(RoutablePageMixin, Page):
    """Page to display all email bulletins."""

    subpage_types = ['BlogEntry']

    @route(r'^$')
    def paginated_blog_entries(self, request, *args, **kwargs):
        """Return paginated bulletins home page."""
        template_name = 'blog/blog_entries_by_page.html'
        context = super(BlogHomePage, self).get_context(request)
        all_blog_entries = BlogEntry.objects.live().order_by('-blog_date')
        paginator = Paginator(all_blog_entries, 5)
        page = request.GET.get('page')
        try:
            resources = paginator.page(page)
        except PageNotAnInteger:
            resources = paginator.page(1)
        except EmptyPage:
            resources = paginator.page(paginator.num_pages)

        context['resources'] = resources
        return render(request, template_name, context)

class BlogEntryTag(TaggedItemBase):
    content_object = ParentalKey('BlogEntry', related_name='tagged_items')


class BlogEntry(OpenGraphMixin, Page):
    """Page for a single blog entry."""

    blog_date = models.DateField("Blog Entry Date")
    blog_author= models.CharField(max_length=255)
    blog_tags = ClusterTaggableManager(through=BlogEntryTag, blank=True)

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
        MultiFieldPanel([
                FieldPanel('blog_date'),
                FieldPanel('blog_author'),
                FieldPanel('blog_tags'),
                ],heading="Blog information"),
        StreamFieldPanel('body'),
    ]

    def save(self, *args, **kwargs):
        """Override to have a more specific slug w/ date & title."""
        self.slug = "{0}-{1}".format(self.blog_date.strftime("%Y-%m-%d"), slugify(self.title))
        super().save(*args, **kwargs)

class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogEntry.objects.live().filter(blog_tags__name=tag)
        #blogpages = BlogEntry.objects.live()

        # Update template context
        context = super(BlogTagIndexPage, self).get_context(request)
        context['blogpages'] = blogpages
        return context
