from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0005_seed_premium_portal_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="leader_photo",
            field=models.FileField(blank=True, upload_to="leaders/"),
        ),
    ]
