# Generated by Django 5.1.2 on 2024-10-14 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="cover_art",
            field=models.FileField(blank=True, upload_to="covers"),
        ),
    ]