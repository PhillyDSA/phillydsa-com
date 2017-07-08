# -*- coding: utf-8 -*-
from wagtail.contrib.modeladmin.options import (
    modeladmin_register,
    ModelAdmin
)
from member_calendar.models import MemberCalendarEvent


class MemberCalendarEventModelAdmin(ModelAdmin):
    """Override default ModelAdmin to order by date."""

    model = MemberCalendarEvent
    menu_label = 'Calendar'
    menu_icon = 'date'
    menu_order = 200
    exclude_from_explorer = False

    list_display = ('title',
                    'event_date',
                    'live',
                    'latest_revision_created_at')
    search_fields = ('title',)
    admin_order_field = 'event_date'
    ordering = ['-event_date']


modeladmin_register(MemberCalendarEventModelAdmin)
