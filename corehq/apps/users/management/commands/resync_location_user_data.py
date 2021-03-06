from django.core.management.base import BaseCommand

from dimagi.utils.couch.database import iter_docs

from corehq.apps.locations.models import SQLLocation
from corehq.apps.users.models import CommCareUser


class Command(BaseCommand):
    help = "Re-syncs location user data for all mobile workers in the domain."

    def add_arguments(self, parser):
        parser.add_argument('domain')

    def process_user(self, user):
        if user.location_id:
            user.set_location(SQLLocation.objects.get(location_id=user.location_id))
        else:
            user.unset_location()

    def handle(self, domain, **options):
        ids = (
            CommCareUser.ids_by_domain(domain, is_active=True) +
            CommCareUser.ids_by_domain(domain, is_active=False)
        )
        for doc in iter_docs(CommCareUser.get_db(), ids):
            user = CommCareUser.wrap(doc)
            try:
                self.process_user(user)
            except Exception as e:
                print("Error processing user %s: %s" % (user._id, e))
