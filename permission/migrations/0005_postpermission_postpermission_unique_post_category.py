# Generated by Django 5.0.3 on 2024-04-05 16:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_rename_user_blogpost_author'),
        ('permission', '0004_alter_category_name_alter_permission_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='permission.category')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='permission.permission')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blogpost')),
            ],
            options={
                'db_table': 'post_category_permissions',
            },
        ),
        migrations.AddConstraint(
            model_name='postpermission',
            constraint=models.UniqueConstraint(fields=('post', 'category'), name='unique_post_category'),
        ),
    ]
