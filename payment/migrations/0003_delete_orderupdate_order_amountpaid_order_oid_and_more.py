# Generated by Django 4.2.16 on 2024-09-10 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_orderupdate_rename_orders_order_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderUpdate',
        ),
        migrations.AddField(
            model_name='order',
            name='amountpaid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='oid',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='order',
            name='paymentstatus',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
