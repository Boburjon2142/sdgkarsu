from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0006_sitesettings_leader_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="leader_name",
            field=models.CharField(default="Nabiyev Dilmurod Xamidullayevich", max_length=120),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="leader_title",
            field=models.CharField(
                default="Qarshi davlat universiteti rektori, iqtisod fanlari doktori, professor",
                max_length=120,
            ),
        ),
    ]
