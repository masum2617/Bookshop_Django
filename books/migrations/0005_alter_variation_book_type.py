# Generated by Django 3.2 on 2021-08-15 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20210815_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='book_type',
            field=models.CharField(choices=[('Cover', 'Cover')], max_length=30, null=True),
        ),
    ]