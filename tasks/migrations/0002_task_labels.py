# Generated by Django 5.1.1 on 2024-10-10 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("labels", "0001_initial"),
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="labels",
            field=models.ManyToManyField(to="labels.label"),
        ),
    ]