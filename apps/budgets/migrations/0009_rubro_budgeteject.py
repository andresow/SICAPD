# Generated by Django 3.0.8 on 2020-10-07 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0008_operation_contraoperarname'),
    ]

    operations = [
        migrations.AddField(
            model_name='rubro',
            name='budgetEject',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
    ]