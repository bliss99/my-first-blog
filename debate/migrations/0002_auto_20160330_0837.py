# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 23:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('debate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('depth', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('modifid_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('parent_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='debate.Category')),
            ],
        ),
        migrations.CreateModel(
            name='OpinionLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stance', models.IntegerField(default=0)),
                ('child_opinion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_opinion', to='debate.Opinion')),
                ('parent_opinion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_opinion', to='debate.Opinion')),
            ],
        ),
        migrations.AddField(
            model_name='agenda',
            name='depth',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='agenda',
            name='parent_agenda',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='debate.Agenda'),
        ),
        migrations.AddField(
            model_name='agenda',
            name='category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='debate.Category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opinion',
            name='ref_opinion',
            field=models.ManyToManyField(related_name='reference', through='debate.OpinionLink', to='debate.Opinion'),
        ),
    ]
