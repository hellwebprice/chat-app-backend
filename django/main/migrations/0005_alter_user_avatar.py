# Generated by Django 4.2.4 on 2023-08-29 16:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_user_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                null=True, upload_to="avatar/%Y-%m-%d-%H-%M-S/", verbose_name="Avatar"
            ),
        ),
    ]
