# Generated by Django 5.0.2 on 2024-03-15 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0005_alter_pedido_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='fecha_pedido',
            field=models.DateTimeField(auto_now=True),
        ),
    ]