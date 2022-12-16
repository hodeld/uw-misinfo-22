# Generated by Django 4.1.2 on 2022-12-07 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misinfo_main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper_sesc',
            name='comment',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='paper_sesc',
            name='in_scope',
            field=models.BooleanField(default=False),
        ),
    ]
