# Generated by Django 2.2.5 on 2022-01-26 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_algorithm'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlgorithmImage',
            fields=[
                ('image_no', models.AutoField(primary_key=True, serialize=False)),
                ('image_root', models.CharField(max_length=1000)),
                ('image_name', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'algorithm_image',
                'managed': False,
            },
        ),
    ]