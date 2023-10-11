# Generated by Django 4.1.7 on 2023-10-03 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Login', '0020_materiaal_leerling'),
    ]

    operations = [
        migrations.AddField(
            model_name='leerling',
            name='gebruiker',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='LeerlingVakRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cijfer', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], default=5)),
                ('beschrijving', models.TextField(default='Schrijf hier een beschrijving van het vak')),
                ('leerling', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Login.leerling')),
                ('vak', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Login.vak')),
            ],
            options={
                'unique_together': {('leerling', 'vak')},
            },
        ),
        migrations.AddField(
            model_name='leerling',
            name='vakken',
            field=models.ManyToManyField(related_name='leerlingen', through='Login.LeerlingVakRating', to='Login.vak'),
        ),
    ]
