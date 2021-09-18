from functools import reduce


def template_time(month=0, days=0, hours=0, minutes=0):
    template_month = f'{month} months' if month > 1 else f'{month} month' if 0 < month <= 1 else ""
    template_days = f'{days} days' if 0 < days < 30 else ""
    template_hours = f'{hours} hours' if hours > 0 else ""
    template_minutes = f'{" and " if template_hours  else ""}{minutes} minutes' if minutes > 0 else ""

    final_template = [
        f"{template_month}, " if template_month else "",
        f"{template_days}, " if template_days else "",
        f"{template_hours}" if template_hours else "",
        template_minutes if not hours else ""
    ]

    return reduce(lambda prev, curr: f'{prev}{curr}', final_template, '')
