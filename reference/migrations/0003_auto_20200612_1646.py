# Generated by Django 3.0.7 on 2020-06-12 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0002_auto_20200612_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='link',
            field=models.URLField(),
        ),
    ]