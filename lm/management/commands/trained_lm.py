from django.core.management.base import BaseCommand, CommandError
from lm.models import LM
from django.utils import timezone

class Command(BaseCommand):
    args = '<lm_id lm_id ...>'
    help = 'Marks the specified LM as trained'

    def handle(self, *args, **options):
        for lm_id in args:
            try:
                lm = LM.objects.get(pk=int(lm_id))
            except LM.DoesNotExist:
                raise CommandError('LM "%s" does not exist' % lm_id)

            lm.status = LM.TRAINED
            lm.last_trained = timezone.now()
            lm.save()

            self.stdout.write('LM "%s" is trained' % lm_id)