# Generated by Django 2.2.23 on 2021-09-25 22:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20210925_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewform',
            name='essay',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Essay rating of candidate (0 - 10)', validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)], verbose_name='Essay'),
        ),
        migrations.AlterField(
            model_name='reviewform',
            name='extracurriculars',
            field=models.PositiveSmallIntegerField(help_text='Extracurriculars rating of candidate (0 - 10)', validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)], verbose_name='Extracurriculars'),
        ),
        migrations.AlterField(
            model_name='reviewform',
            name='interview',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Interview rating of candidate (0 - 10)', validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)], verbose_name='Interview'),
        ),
        migrations.AlterField(
            model_name='reviewform',
            name='leadership',
            field=models.PositiveIntegerField(help_text='Leadership rating of candidate (0 - 10)', validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)], verbose_name='Leadership'),
        ),
        migrations.AlterField(
            model_name='reviewform',
            name='recLetters',
            field=models.PositiveSmallIntegerField(help_text='RecLetters rating of candidate (0 - 10)', validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)], verbose_name='RecLetters'),
        ),
    ]
