from django.core.management.base import BaseCommand, CommandError
from experiments.models import Experiment
from django.utils import timezone

class Command(BaseCommand):
    args = '<experiment_id ...>'
    help = 'Sets the given experiment\'s status as finished'

    def handle(self, *args, **options):
    	exp_id = args[0]
        try:
            exp = Experiment.objects.get(pk=int(exp_id))
        except Experiment.DoesNotExist:
            raise CommandError('Experiment "%s" does not exist' % exp_id)
        
        exp.status = Experiment.FINISHED
        exp.save()
        
        self.stdout.write('Set experiment {0} as trained'.format(exp.id))
