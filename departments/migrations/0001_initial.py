# Generated by Django 2.1.4 on 2019-01-20 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomor', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=140)),
                ('dep', models.CharField(max_length=100, verbose_name='Department')),
                ('div', models.CharField(max_length=100, verbose_name='Division')),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='departments.Division')),
            ],
        ),
    ]
