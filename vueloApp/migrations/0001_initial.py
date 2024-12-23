# Generated by Django 5.1 on 2024-11-04 05:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aerolinea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=10)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Asiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=5)),
                ('disponible', models.BooleanField(default=True)),
                ('precio', models.DecimalField(decimal_places=2, default=80000, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('mensaje', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_salida', models.TimeField()),
                ('hora_llegada', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Boleto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('rut', models.CharField(max_length=12)),
                ('total_viaje', models.DecimalField(decimal_places=2, max_digits=10)),
                ('aerolinea', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='vueloApp.aerolinea')),
                ('asiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vueloApp.asiento')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('horario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vueloApp.horario')),
                ('destino_ida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destino_ida', to='vueloApp.pais')),
                ('destino_vuelta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destino_vuelta', to='vueloApp.pais')),
            ],
        ),
    ]
