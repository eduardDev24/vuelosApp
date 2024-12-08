# Generated by Django 5.1 on 2024-11-19 06:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vueloApp', '0002_contacto_fecha'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='boleto',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boletos_vuelo', to=settings.AUTH_USER_MODEL),
        ),
    ]