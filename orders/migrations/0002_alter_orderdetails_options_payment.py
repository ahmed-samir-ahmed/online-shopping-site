# Generated by Django 4.2.7 on 2023-11-14 14:49

import creditcards.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderdetails',
            options={'ordering': ['-id']},
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipment_address', models.CharField(max_length=100)),
                ('shipment_phone', models.CharField(max_length=100)),
                ('card_number', creditcards.models.CardNumberField(max_length=25)),
                ('expire', creditcards.models.CardExpiryField()),
                ('security', creditcards.models.SecurityCodeField(max_length=4)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
        ),
    ]
