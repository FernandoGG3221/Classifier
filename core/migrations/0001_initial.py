# Generated by Django 2.1 on 2020-06-15 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Contenido')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Link de video')),
                ('images', models.FileField(blank=True, null=True, upload_to='', verbose_name='Imagenes para el carrusel')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creado el')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Actualizado el')),
            ],
        ),
    ]