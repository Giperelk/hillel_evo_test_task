# Generated by Django 4.2.6 on 2023-10-24 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_user_login_last_time_alter_user_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_request',
            field=models.DateTimeField(null=True),
        ),
    ]
