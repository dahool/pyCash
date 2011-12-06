from django.core.management.base import BaseCommand
from cash.services.SyncService import SyncServiceClass

class Command(BaseCommand):
    help = 'Sync Expenses'

    def handle(self, *args, **options):
        self.stdout.write("Syncing ...\n")
        sync = SyncServiceClass()
        try:
            r = sync.sync_expenses()
        except Exception, e:
            self.stdout.write("Error: %s\n" % str(e))
        else:
            self.stdout.write("Received %d elements.\n" % r)