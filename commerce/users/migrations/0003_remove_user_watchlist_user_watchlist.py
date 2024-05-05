# Generated by Django 5.0.3 on 2024-04-20 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_alter_auction_category'),
        ('users', '0002_user_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='watchlist',
        ),
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(null=True, related_name='followed_auctions', to='auctions.auction'),
        ),
    ]
