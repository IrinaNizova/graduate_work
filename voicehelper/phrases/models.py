from django.db import models
from django.utils.translation import gettext_lazy as _
from django_better_admin_arrayfield.models.fields import ArrayField


class CommandPhrases(models.Model):
    name = models.CharField(max_length=100)
    values = ArrayField(models.CharField(max_length=200))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('ключевая фраза')
        verbose_name_plural = _('ключевые фразы')


class PhraseType(models.Model):
    type = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('вид фраз')
        verbose_name_plural = _('виды фраз')


class VariousPhases(models.Model):
    type = models.ForeignKey(PhraseType, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = _('фраза')
        verbose_name_plural = _('одтельные фразы')
