# Generated by Django 3.2 on 2021-08-15 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_alter_cart_item_book_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart_item',
            name='book_type',
            field=models.CharField(max_length=20, null=True),
        ),
    ]