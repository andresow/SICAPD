# Generated by Django 3.0.8 on 2020-09-21 23:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0002_rubro_imported'),
    ]

    operations = [
        migrations.AddField(
            model_name='movement',
            name='typeAgreement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.TypeAgreement'),
        ),
    ]
