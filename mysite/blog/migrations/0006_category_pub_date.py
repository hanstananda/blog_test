# Generated by Django 2.1.1 on 2018-09-17 14:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comments_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 17, 22, 50, 12, 523233), verbose_name='date created'),
            preserve_default=False,
        ),
    ]
