# Generated by Django 4.1 on 2024-04-27 07:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0007_amenities_provides_interests_amenitiesin_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="provides",
            name="building_name",
        ),
        migrations.RemoveField(
            model_name="provides",
            name="company_name",
        ),
    ]
