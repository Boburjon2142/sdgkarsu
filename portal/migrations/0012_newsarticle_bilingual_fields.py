from django.db import migrations, models


def copy_legacy_newsarticle_content(apps, schema_editor):
    NewsArticle = apps.get_model("portal", "NewsArticle")
    for article in NewsArticle.objects.all():
        article.title_uz = article.title_uz or article.title or ""
        article.title_en = article.title_en or article.title or ""
        article.summary_uz = article.summary_uz or article.summary or ""
        article.summary_en = article.summary_en or article.summary or ""
        article.body_uz = article.body_uz or article.body or ""
        article.body_en = article.body_en or article.body or ""
        article.save(
            update_fields=[
                "title_uz",
                "title_en",
                "summary_uz",
                "summary_en",
                "body_uz",
                "body_en",
            ]
        )


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0011_newsarticle_sdg_goal"),
    ]

    operations = [
        migrations.AddField(
            model_name="newsarticle",
            name="body_en",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="newsarticle",
            name="body_uz",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="newsarticle",
            name="summary_en",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="newsarticle",
            name="summary_uz",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="newsarticle",
            name="title_en",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="newsarticle",
            name="title_uz",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.RunPython(copy_legacy_newsarticle_content, migrations.RunPython.noop),
    ]
