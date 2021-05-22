from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from .models import CommandPhrases, PhraseType, VariousPhases

admin.site.register(PhraseType)
admin.site.register(VariousPhases)


@admin.register(CommandPhrases)
class CommandPhrasesAdmin(admin.ModelAdmin, DynamicArrayMixin):
    ordering = ('name',)
