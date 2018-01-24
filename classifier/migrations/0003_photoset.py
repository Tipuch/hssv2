# Generated by Django 2.0.1 on 2018-01-23 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0010_auto_20160105_1307'),
        ('classifier', '0002_auto_20180122_2006'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('title', models.CharField(max_length=250, unique=True, verbose_name='title')),
                ('slug', models.SlugField(help_text='A "slug" is a unique URL-friendly title for an object.', max_length=250, unique=True, verbose_name='title slug')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('gallery', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='photo_set', to='photologue.Gallery', verbose_name='gallery')),
            ],
        ),
    ]