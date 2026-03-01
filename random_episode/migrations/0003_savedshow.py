# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("random_episode", "0002_profile"),
    ]

    operations = [
        migrations.CreateModel(
            name="SavedShow",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tvdb_show_id", models.IntegerField()),
                ("show_name", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="saved_shows", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name="savedshow",
            constraint=models.UniqueConstraint(fields=("user", "tvdb_show_id"), name="unique_user_saved_show"),
        ),
    ]
