# Generated by Django 3.0.8 on 2020-07-22 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userinterests'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserInterests',
            new_name='UserInterest',
        ),
    ]
