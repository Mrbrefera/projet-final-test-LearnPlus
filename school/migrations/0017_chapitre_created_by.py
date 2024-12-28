# Generated by Django 2.2.12 on 2024-12-27 02:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0016_matiere_instructor'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapitre',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chapitres_crees', to=settings.AUTH_USER_MODEL),
        ),
    ]
