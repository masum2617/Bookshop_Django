# Generated by Django 3.2 on 2021-08-15 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_variation_book_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='book_type',
            field=models.CharField(choices=[('cover', 'cover')], max_length=30, null=True),
        ),
    ]