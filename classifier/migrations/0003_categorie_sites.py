# Generated by Django 2.0 on 2018-01-12 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('classifier', '0002_remove_categorie_sites'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorie',
            name='sites',
            field=models.ManyToManyField(blank=True, to='sites.Site', verbose_name='sites'),
        ),
    ]
