# Generated by Django 5.1.5 on 2025-02-01 01:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbcs', '0009_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='child_school',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parentslist', to='rbcs.schools'),
        ),
    ]
