# Generated by Django 2.0 on 2018-01-11 23:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classifier', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorie',
            name='sites',
        ),
    ]
