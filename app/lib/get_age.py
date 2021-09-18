import math

from .template_time import template_time


def get_age(total_seconds: int):
    SECONDS_IN_MINUTES = 60
    SECONDS_IN_HOUR = 60 * 60
    SECONDS_IN_DAY = SECONDS_IN_HOUR * 24

    days = math.floor(total_seconds // SECONDS_IN_DAY)

    month = days // 30

    hours = math.floor(
        (total_seconds - (days * SECONDS_IN_DAY)) // SECONDS_IN_HOUR)
    minutes = math.floor((total_seconds - (days * SECONDS_IN_DAY) -
                         (hours * SECONDS_IN_HOUR)) // SECONDS_IN_MINUTES)

    return template_time(month, days, hours, minutes)
