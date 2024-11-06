# Generated by Django 5.1.3 on 2024-11-06 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('fname', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
            ],
        ),
    ]
