from django.db import migrations


OLD_NAME = "Aziza Mamatova"
NEW_NAME = "Ismatov Xolmumin Xurozovich"
TARGET_DEPARTMENT = "Strategic Coordination Office"


def update_contact_name(apps, schema_editor):
    DepartmentContact = apps.get_model("portal", "DepartmentContact")
    DepartmentContact.objects.filter(
        department_name=TARGET_DEPARTMENT,
        contact_person=OLD_NAME,
    ).update(contact_person=NEW_NAME)


def revert_contact_name(apps, schema_editor):
    DepartmentContact = apps.get_model("portal", "DepartmentContact")
    DepartmentContact.objects.filter(
        department_name=TARGET_DEPARTMENT,
        contact_person=NEW_NAME,
    ).update(contact_person=OLD_NAME)


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0012_newsarticle_bilingual_fields"),
    ]

    operations = [
        migrations.RunPython(update_contact_name, revert_contact_name),
    ]
