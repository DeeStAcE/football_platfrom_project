# Generated by Django 4.2.1 on 2023-05-22 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("football", "0002_alter_player_position"),
    ]

    operations = [
        migrations.AlterField(
            model_name="player",
            name="team",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="football.team",
            ),
        ),
    ]
