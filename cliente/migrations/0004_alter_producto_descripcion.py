# Generated by Django 5.0.2 on 2024-03-14 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0003_alter_pedido_producto_precio_producto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='descripcion',
            field=models.TextField(),
        ),
    ]
