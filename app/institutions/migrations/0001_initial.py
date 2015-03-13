# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'Correo Electronico', db_index=True)),
                ('full_name', models.CharField(max_length=40, verbose_name=b'Nombre Completo')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('slug', models.SlugField(default=b'', unique=True, editable=False)),
                ('description', models.TextField()),
                ('created', models.DateField()),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('url', models.URLField(null=True, blank=True)),
                ('cost', models.CharField(max_length=18, null=True, blank=True)),
                ('categories', models.ManyToManyField(to='institutions.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=75)),
                ('province', models.CharField(max_length=24)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, verbose_name=b'Nombre de la Institucion')),
                ('slug', models.SlugField(default=b'', unique=True, editable=False)),
                ('url', models.URLField(max_length=255, null=True, verbose_name=b'Pagina Web', blank=True)),
                ('description', models.TextField(null=True, verbose_name=b'Descripcion', blank=True)),
                ('logo', models.ImageField(null=True, upload_to=b'profile_pics', blank=True)),
                ('phone', models.CharField(max_length=10, null=True, blank=True)),
                ('address', models.CharField(max_length=100, null=True, verbose_name=b'Direccion', blank=True)),
                ('province', models.CharField(blank=True, max_length=100, null=True, choices=[(b'Distrito Nacional', b'Distrito Nacional'), (b'Altagracia', b'Altagracia'), (b'Azua', b'Azua'), (b'Bahoruco', b'Bahoruco'), (b'Barahona', b'Barahona'), (b'Dajabon', b'Dajabon'), (b'Duarte', b'Duarte'), (b'El Seybo', b'El Seybo'), (b'Elias Pi\xc3\xb1a', b'Elias Pi\xc3\xb1a'), (b'Espaillat', b'Espaillat'), (b'Hato Mayor', b'Hato Mayor'), (b'Independencia', b'Independencia'), (b'La Romana', b'La Romana'), (b'La Vega', b'La Vega'), (b'Maria Trinidad Sanchez', b'Maria Trinidad Sanchez'), (b'Monse\xc3\xb1or Nouel', b'Monse\xc3\xb1or Nouel'), (b'Montecristi', b'Montecristi'), (b'Monte Plata', b'Monte Plata'), (b'Pedernales', b'Pedernales'), (b'Peravia', b'Peravia'), (b'Puerto Plata', b'Puerto Plata'), (b'Hermanas Mirabal', b'Hermanas Mirabal'), (b'Samana', b'Samana'), (b'San Cristobal', b'San Cristobal'), (b'San Juan', b'San Juan'), (b'San Pedro de Macoris', b'San Pedro de Macoris'), (b'Sanchez Ramirez', b'Sanchez Ramirez'), (b'Santiago de los Caballeros', b'Santiago de los Caballeros'), (b'Santiago Rodriguez', b'Santiago Rodriguez'), (b'Valverde', b'Valverde'), (b'San Jose de Ocoa', b'San Jose de Ocoa'), (b'Santo Domingo', b'Santo Domingo')])),
                ('approved', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('categories', models.ManyToManyField(to='institutions.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='organization',
            field=models.ForeignKey(blank=True, to='institutions.Organization', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='organization',
            field=models.ForeignKey(blank=True, to='institutions.Organization', null=True),
            preserve_default=True,
        ),
    ]
