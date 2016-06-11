import re
from collections import defaultdict


def requests_per_day(log):
    all_dates = re.findall(r'\d{4}-\d{1,2}-\d{1,2}', log)

    dates = defaultdict(int)
    for date in all_dates:
        dates[date] += 1

    return dates


def ips_set(log):
    return set(re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', log))
