# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20151001_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='screenshot',
            field=models.ImageField(default='test', upload_to=b'screenshots'),
            preserve_default=False,
        ),
    ]
