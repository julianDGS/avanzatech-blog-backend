# Generated by Django 5.0.3 on 2024-04-04 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_blogpost_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=models.TextField(default=None, verbose_name='content'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(default=None, max_length=250, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(default=None, verbose_name='comment'),
        ),
    ]
