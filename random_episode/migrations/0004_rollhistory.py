# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("random_episode", "0003_savedshow"),
    ]

    operations = [
        migrations.CreateModel(
            name="RollHistory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tvdb_show_id", models.IntegerField()),
                ("show_name", models.CharField(blank=True, max_length=255)),
                ("season_number", models.PositiveIntegerField()),
                ("episode_number", models.PositiveIntegerField()),
                ("episode_title", models.CharField(blank=True, max_length=255)),
                ("rolled_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="roll_history", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-rolled_at"],
                "verbose_name_plural": "Roll histories",
            },
        ),
    ]
