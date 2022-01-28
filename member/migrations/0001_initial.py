# Generated by Django 2.2.5 on 2022-01-28 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithm',
            fields=[
                ('algo_no', models.AutoField(primary_key=True, serialize=False)),
                ('algo_update', models.DateTimeField()),
                ('algo_title', models.CharField(max_length=50)),
                ('algo_detail', models.TextField()),
            ],
            options={
                'db_table': 'algorithm',
                'managed': False,
            },
        ),
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
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_no', models.AutoField(primary_key=True, serialize=False)),
                ('comment_detail', models.TextField()),
            ],
            options={
                'db_table': 'comment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('likes_no', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'likes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('member_no', models.AutoField(primary_key=True, serialize=False)),
                ('member_email', models.CharField(max_length=50)),
                ('member_name', models.CharField(max_length=10)),
                ('member_password', models.CharField(max_length=20)),
                ('member_joindate', models.DateTimeField()),
                ('admin_flag', models.IntegerField(default=0)),
                ('member_status', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'member',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('sol_no', models.AutoField(primary_key=True, serialize=False)),
                ('sol_detail', models.TextField()),
                ('sol_like', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'solution',
                'managed': False,
            },
        ),
    ]
