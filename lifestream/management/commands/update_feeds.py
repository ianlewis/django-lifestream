#:coding=utf-8:

from django.core.management.base import BaseCommand

from lifestream.feeds import update_feeds

#Command to update feeds
class Command(BaseCommand):
    def handle(self, *args, **options):
        update_feeds()
