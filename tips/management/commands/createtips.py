import re
import csv
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime as dt
from tips.models import Tips, Links, Tags


link = re.compile(r"\bhttp(?:s)?:\S*\b")
tag = re.compile(r"#\b.+?\b")


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
        # parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        with open('Daily Python Tips.csv', 'r', newline='', encoding='utf-8') as fh:
            data = csv.reader(fh, delimiter=',')
            data = (i for i in data)
            for d in data:
                try:
                    p = '%m/%d/%Y %H:%M:%S'
                    ts = dt.strptime(d[0], p)
                except (TypeError, ValueError):
                    p = '%m/%d/%Y %H:%M'
                    ts = dt.strptime(d[0], p)
                try:
                    tags = re.findall(tag, d[1])
                    links = re.findall(link, d[1])
                    tags = [t.strip('#').title() for t in tags]
                    tagmds = [Tags.objects.update_or_create(name=t, defaults={'name': t})[0] for t in tags]
                    tipmd = Tips.objects.create(timestamp=ts, tip=d[1], account=d[2].strip('@'), email=d[3])
                    linkmds = [Links.objects.update_or_create(name=i, tip=tipmd, defaults={'name': i, 'tip': tipmd})[1] for i in links if tipmd]
                    tipmd.tags.add(*tagmds)
                    tipmd.save()
                except Exception as err:
                    self.stderr.write(err)
