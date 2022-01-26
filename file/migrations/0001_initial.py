# Generated by Django 2.2.5 on 2022-01-26 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('file_no', models.AutoField(primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=50)),
                ('file_date', models.DateTimeField()),
                ('file_volume', models.BigIntegerField()),
                ('file_root', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'file',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FileList',
            fields=[
                ('file_file', models.AutoField(primary_key=True, serialize=False)),
                ('file_root', models.CharField(max_length=1000)),
                ('file_name', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'file_list',
                'managed': False,
            },
        ),
    ]