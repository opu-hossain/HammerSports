# Generated by Django 5.0.6 on 2024-05-29 08:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Blog", "0002_alter_comment_author"),
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="followed_categories",
            field=models.ManyToManyField(related_name="followers", to="Blog.category"),
        ),
    ]
