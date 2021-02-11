# Generated by Django 2.2.10 on 2021-02-11 15:16

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0004_auto_20210211_1454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='user_id',
        ),
        migrations.AddField(
            model_name='answer',
            name='date_answered',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 2, 11, 15, 16, 20, 405337, tzinfo=utc), verbose_name='Date answered'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='surveys.Question'),
        ),
        migrations.CreateModel(
            name='CompletedSurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(verbose_name='User ID')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.Survey')),
            ],
            options={
                'verbose_name': 'Completed survey',
                'verbose_name_plural': 'Completed surveys',
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='completed_survey',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='surveys.CompletedSurvey'),
        ),
    ]
