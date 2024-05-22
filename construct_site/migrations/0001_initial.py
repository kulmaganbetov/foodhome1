# Generated by Django 3.1.4 on 2021-02-07 14:07

from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0021_site_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element_id', models.CharField(max_length=40)),
                ('photo', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='images/')),
                ('value', models.TextField(blank=True, null=True)),
                ('user_site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.usersite')),
            ],
        ),
    ]
