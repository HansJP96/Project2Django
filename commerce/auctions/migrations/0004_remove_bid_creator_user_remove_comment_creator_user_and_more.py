# Generated by Django 5.0.3 on 2024-04-05 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_creator_user_auction_seller_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='creator_user',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='creator_user',
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(max_length=256),
        ),
        migrations.AlterField(
            model_name='comment',
            name='response',
            field=models.TextField(max_length=256, null=True),
        ),
    ]
