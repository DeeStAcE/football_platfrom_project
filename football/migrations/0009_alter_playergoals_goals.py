# Generated by Django 4.2.1 on 2023-05-23 14:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("football", "0008_playergoals_match_goal_scorers"),
    ]

    operations = [
        migrations.AlterField(
            model_name="playergoals",
            name="goals",
            field=models.SmallIntegerField(),
        ),
    ]