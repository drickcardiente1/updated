# Generated by Django 4.1.6 on 2023-02-28 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]