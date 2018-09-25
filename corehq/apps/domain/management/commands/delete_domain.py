from __future__ import print_function

from __future__ import absolute_import
from __future__ import unicode_literals
from django.core.management.base import BaseCommand

from corehq.apps.domain.models import Domain
from corehq.apps.es import AppES, CaseES, CaseSearchES, DomainES, FormES, GroupES, LedgerES, UserES
from six.moves import input


class Command(BaseCommand):
    help = "Deletes the given domain and its contents"

    def add_arguments(self, parser):
        parser.add_argument(
            'domain_name',
        )
        parser.add_argument(
            '--noinput',
            action='store_true',
            dest='noinput',
            default=False,
            help='Skip important confirmation warnings.',
        )

    def handle(self, domain_name, **options):
        domain = Domain.get_by_name(domain_name)
        if not domain:
            print('domain with name "{}" not found'.format(domain_name))
            return
        if not options['noinput']:
            confirm = input(
                """
                Are you sure you want to delete the domain "{}" and all of it's data?
                This operation is not reversible and all forms and cases will be PERMANENTLY deleted.

                Type the domain's name again to continue, or anything else to cancel:
                """.format(domain_name)
            )
            if confirm != domain_name:
                print("\n\t\tDomain deletion cancelled.")
                return

        for hqESQuery in [AppES, CaseES, CaseSearchES, DomainES, FormES, GroupES, LedgerES, UserES]:
            assert hqESQuery().domain(domain_name).run().total == 0, '%s contains data' % hqESQuery.index

        print("Deleting domain {}".format(domain_name))
        domain.delete()
        print("Operation completed")
