# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-06-26 17:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170626_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='photo',
            field=models.ImageField(default='user1.jpg', upload_to='photos'),
        ),
    ]
