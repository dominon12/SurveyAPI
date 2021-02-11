# Generated by Django 2.2.10 on 2021-02-11 14:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('date_started', models.DateTimeField(auto_now_add=True, verbose_name='Date started')),
                ('date_ended', models.DateTimeField(verbose_name='Date ended')),
            ],
            options={
                'verbose_name': 'Survey',
                'verbose_name_plural': 'Surveys',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text')),
                ('question_type', models.IntegerField(choices=[(1, 'Text answer'), (2, '1 choice answer'), (3, 'Multiple choices answer')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)], verbose_name="Question's type")),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.Survey')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
    ]