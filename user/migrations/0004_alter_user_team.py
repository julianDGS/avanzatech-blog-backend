# Generated by Django 5.0.3 on 2024-04-04 22:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_team_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='user.team'),
        ),
    ]
