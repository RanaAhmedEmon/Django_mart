# Generated by Django 4.2.16 on 2024-09-16 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_order_zip_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]