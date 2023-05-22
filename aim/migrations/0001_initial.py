# Generated by Django 3.2.16 on 2023-05-12 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(default='123456', max_length=255)),
                ('user_auth', models.CharField(default='user', max_length=255)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'user',
                'managed': (True,),
            },
        ),
    ]
