# Generated by Django 4.1.6 on 2023-02-28 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_profile_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Employee',
        ),
    ]