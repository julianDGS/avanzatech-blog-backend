# Generated by Django 5.0.3 on 2024-05-28 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_blogpost_author_alter_like_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='like',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
