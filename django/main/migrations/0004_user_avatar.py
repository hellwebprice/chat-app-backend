# Generated by Django 4.2.4 on 2023-08-29 16:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0003_user_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.ImageField(null=True, upload_to="", verbose_name="Avatar"),
        ),
    ]
