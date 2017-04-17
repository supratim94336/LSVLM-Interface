from django.contrib import admin
from corpora.models import Lang, Corpus, CountFile

# Register your models here.
admin.site.register(Lang)
admin.site.register(Corpus)

class CountFileAdmin(admin.ModelAdmin):
    readonly_fields = ('corpus', 'm')
    list_display = ('corpus', 'm')
admin.site.register(CountFile, CountFileAdmin)
