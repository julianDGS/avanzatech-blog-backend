# Generated by Django 5.0.3 on 2024-05-28 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0008_alter_postpermission_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='permission',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
