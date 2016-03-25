from django.db import models
from django.utils import timezone


class Agenda(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    modifid_date = models.DateTimeField(default=timezone.now)

    def offer(self):
        self.save()

    def __str__(self):
        return self.text[:100] + "..."

class Opinion(models.Model):
    author = models.ForeignKey('auth.User')
    agenda = models.ForeignKey('Agenda')
    stance = models.IntegerField(default=0)	#10: 찬성, 90:반대
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    modifid_date = models.DateTimeField(default=timezone.now)

    def offer(self):
        self.save()

    def __str__(self):
        return self.text[:100] + "..."
