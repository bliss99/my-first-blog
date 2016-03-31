from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=50)
    parent_category = models.ForeignKey('self', null=True, blank=True)
    depth = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    modifid_date = models.DateTimeField(default=timezone.now)
    
    def  __str__(self):
        return self.name


class Agenda(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    modifid_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey('Category')
    parent_agenda = models.ForeignKey('self', null=True, blank=True)
    depth = models.IntegerField(default=0)

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
    ref_opinion = models.ManyToManyField('self', through='OpinionLink', 
        symmetrical=False, related_name='reference')

    def offer(self):
        self.save()

    def __str__(self):
        return self.text[:100] + "..."


class OpinionLink(models.Model):
    parent_opinion = models.ForeignKey('Opinion', related_name='parent_opinion')
    child_opinion = models.ForeignKey('Opinion', related_name='child_opinion')
    stance = models.IntegerField(default=0) #10: 찬성, 90:반대

    def  __str__(self):
        return self.parent_opinion.text + " : " +str(self.stance) + " to " + self.child_opinion.text

