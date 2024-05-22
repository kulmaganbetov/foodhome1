# Generated by Django 3.1.4 on 2021-01-29 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_remove_site_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='bacground_color',
            field=models.CharField(default='#25d366', max_length=120),
        ),
        migrations.AddField(
            model_name='support',
            name='icon_color',
            field=models.CharField(default='#ffffff', max_length=120),
        ),
        migrations.AddField(
            model_name='support',
            name='text_color',
            field=models.CharField(default='#ffffff', max_length=120),
        ),
    ]