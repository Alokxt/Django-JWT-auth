# Generated by Django 5.1.5 on 2025-02-01 00:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbcs', '0007_newus'),
    ]

    operations = [
        migrations.DeleteModel(
            name='newus',
        ),
        migrations.AddField(
            model_name='achievements',
            name='st_school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_achievements', to='rbcs.schools'),
        ),
    ]
