# Generated by Django 4.1.2 on 2022-12-15 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misinfo_main', '0005_alter_paper_sesc_paperclass'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper_sesc',
            name='title',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
