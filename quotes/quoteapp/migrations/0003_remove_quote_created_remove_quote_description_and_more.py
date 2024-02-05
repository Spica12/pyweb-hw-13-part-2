# Generated by Django 5.0.1 on 2024-01-07 13:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0002_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='created',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='description',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='done',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='name',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='user',
        ),
        migrations.AddField(
            model_name='quote',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='quoteapp.author'),
        ),
        migrations.AddField(
            model_name='quote',
            name='quote',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
