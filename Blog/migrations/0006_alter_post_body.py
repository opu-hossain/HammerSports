# Generated by Django 5.0.6 on 2024-05-27 01:13

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Blog", "0005_alter_post_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="body",
            field=django_ckeditor_5.fields.CKEditor5Field(),
        ),
    ]
