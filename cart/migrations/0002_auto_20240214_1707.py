# Generated by Django 3.2.4 on 2024-02-14 11:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 14, 11, 57, 40, 179294, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('accepted', 'Заказ принят'), ('in_progress', 'Заказ делается'), ('courier', 'Передан курьеру'), ('delivered', 'Доставлен'), ('arrived', 'Прибыл')], default='accepted', max_length=50),
        ),
    ]
