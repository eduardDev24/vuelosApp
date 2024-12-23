# Generated by Django 5.1 on 2024-11-19 06:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packApp2', '0002_carrito'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='pack_promocion',
            name='nombre',
            field=models.CharField(default='Sin nombre', max_length=100),
        ),
        migrations.CreateModel(
            name='boleto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pack', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='packApp2.pack_promocion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boletos_pack', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
