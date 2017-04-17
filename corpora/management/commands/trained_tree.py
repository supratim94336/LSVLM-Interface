from django.core.management.base import BaseCommand, CommandError
from corpora.models import Corpus, CountFile
from django.utils import timezone

class Command(BaseCommand):
    args = '<corpus_id m ...>'
    help = 'Creates the count file for the given corpus and n'

    def handle(self, *args, **options):
        self.stdout.write(str(args))
	corpus_id = args[0]
        m = args[1]
        
        try:
            corpus = Corpus.objects.get(pk=int(corpus_id))
        except Corpus.DoesNotExist:
            raise CommandError('Corpus "%s" does not exist' % corpus_id)
        
        count_file = CountFile(corpus = corpus, m = m)
        count_file.save()
        
        self.stdout.write('Created {0}-count tree for corpus {1}'.format(m, corpus.name))
