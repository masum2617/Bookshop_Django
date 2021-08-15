# Generated by Django 3.2 on 2021-08-15 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_variation_book_type'),
        ('cart', '0003_cart_item_book_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart_item',
            name='type_of_book',
            field=models.ManyToManyField(blank=True, to='books.Variation'),
        ),
    ]
