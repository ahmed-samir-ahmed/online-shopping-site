# Generated by Django 4.2.7 on 2023-11-12 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_products_favorites_userprofile_products_favorite'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='products_favorite',
            new_name='products_favorites',
        ),
    ]