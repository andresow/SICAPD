# Generated by Django 3.0.8 on 2020-09-22 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0005_auto_20200921_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='agreement',
            name='origin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Origin'),
        ),
    ]