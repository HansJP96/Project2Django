# Generated by Django 5.0.3 on 2024-04-19 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_auction_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.IntegerField(blank=True, choices=[(None, '----------'), (1001, 'Uncategorized'), (0, 'Fashion'), (1, 'Toys'), (2, 'Home & Garden'), (3, 'Music'), (4, 'Books & Magazines'), (5, 'Computers/Tablets'), (6, 'Video Games & Consoles')], default=1001),
        ),
    ]
