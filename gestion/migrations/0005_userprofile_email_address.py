# Generated by Django 5.0.1 on 2024-01-30 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0004_alter_userprofile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email_address',
            field=models.EmailField(default='default@example.com', max_length=255, unique=True),
        ),
    ]
