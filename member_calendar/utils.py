#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2017 Jeremy Low

"""Utilities for working with calendar app."""

import datetime
import calendar


def make_calendar(year=datetime.datetime.now().year, month=datetime.datetime.now().month):
    """Return curr year & month & list of lists representing days in curr month."""
    calendar.setfirstweekday(calendar.SUNDAY)
    year, month = int(year), int(month)
    return year, month, calendar.monthcalendar(year, month)
