# Generated by Django 3.0.8 on 2020-12-11 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('state', models.CharField(choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')], max_length=100)),
                ('corriente', models.CharField(max_length=100)),
                ('nature', models.CharField(max_length=100)),
                ('typeAccount', models.CharField(choices=[('M', 'M'), ('A', 'A')], max_length=100)),
                ('dateCreation', models.DateField(auto_now_add=True)),
                ('level', models.IntegerField()),
                ('accountFather', models.BigIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AccountPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('state', models.CharField(choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')], max_length=100)),
                ('initialDate', models.DateField()),
                ('finalDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='AccountTypeRubro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeAccount', models.CharField(max_length=100)),
                ('document', models.CharField(max_length=100)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numberAg', models.CharField(max_length=100)),
                ('descriptionAg', models.TextField()),
                ('dateAg', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Bussines',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('nit', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('representative', models.CharField(max_length=100)),
                ('rubroPattern', models.CharField(max_length=100)),
                ('accountPattern', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Inform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameI', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('digitI', models.BigIntegerField()),
                ('bussines', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Bussines')),
            ],
        ),
        migrations.CreateModel(
            name='InformBank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameI', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('digitI', models.BigIntegerField()),
                ('bussines', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Bussines')),
            ],
        ),
        migrations.CreateModel(
            name='InformDetall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codeInfD', models.CharField(max_length=100)),
                ('descriptionInfD', models.TextField()),
                ('activity', models.CharField(max_length=100)),
                ('inform', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Inform')),
            ],
        ),
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameRubro', models.BigIntegerField(null=True)),
                ('concept', models.CharField(max_length=100)),
                ('value', models.BigIntegerField()),
                ('balance', models.BigIntegerField()),
                ('date', models.DateField()),
                ('disponibility', models.BigIntegerField(null=True)),
                ('register', models.BigIntegerField(null=True)),
                ('obligation', models.BigIntegerField(null=True)),
                ('vouchePayment', models.BigIntegerField(null=True)),
                ('budgetEject', models.BigIntegerField(null=True)),
                ('observation', models.TextField(null=True)),
                ('agreement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Agreement')),
                ('bussines', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Bussines')),
            ],
        ),
        migrations.CreateModel(
            name='Origin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameOrigin', models.CharField(max_length=100)),
                ('codeOrigin', models.CharField(max_length=100)),
                ('descriptionOrigin', models.TextField()),
                ('orderOrigin', models.IntegerField()),
                ('finalDateOrigin', models.DateField()),
                ('accountPeriod', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.AccountPeriod')),
            ],
        ),
        migrations.CreateModel(
            name='RubroMovement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BigIntegerField()),
                ('valueP', models.BigIntegerField()),
                ('balance', models.BigIntegerField()),
                ('date', models.DateField()),
                ('nameRubro', models.BigIntegerField()),
                ('bussines', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Bussines')),
                ('movement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Movement')),
            ],
        ),
        migrations.CreateModel(
            name='TypeContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameTC', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('categoryTC', models.CharField(max_length=100)),
                ('digitsTC', models.BigIntegerField()),
                ('bussines', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Bussines')),
            ],
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('order', models.IntegerField()),
                ('number', models.IntegerField()),
                ('category', models.CharField(max_length=100)),
                ('dateCreation', models.DateField()),
                ('bussines', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Bussines')),
            ],
        ),
        migrations.CreateModel(
            name='ValuesAccountObligation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeAccount', models.CharField(max_length=100)),
                ('value', models.BigIntegerField(null=True)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.AccountTypeRubro')),
                ('obligation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.RubroMovement')),
            ],
        ),
        migrations.CreateModel(
            name='TypeContractDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codeTypeC', models.CharField(max_length=100)),
                ('descriptionTypeC', models.TextField()),
                ('activity', models.CharField(max_length=100)),
                ('typeContract', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.TypeContract')),
            ],
        ),
        migrations.CreateModel(
            name='TypeAgreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codeTA', models.CharField(max_length=100)),
                ('nameTA', models.CharField(max_length=100)),
                ('descriptionTA', models.TextField()),
                ('ordenTA', models.IntegerField()),
                ('validacionTA', models.CharField(blank=True, max_length=100)),
                ('mensajeTA', models.CharField(blank=True, max_length=100)),
                ('bussines', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Bussines')),
            ],
        ),
        migrations.CreateModel(
            name='Third',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeIdentification', models.CharField(choices=[('Cédula de Ciudadanía', 'Cédula de Ciudadanía'), ('Cédula Extranjeria', 'Cédula Extrangeria'), ('Pasaporte', 'Pasaporte')], max_length=64)),
                ('identification', models.BigIntegerField()),
                ('name', models.CharField(max_length=100)),
                ('surnames', models.CharField(max_length=100)),
                ('reason', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=100)),
                ('bussines', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Bussines')),
            ],
        ),
        migrations.CreateModel(
            name='RubroBalanceOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeOperation', models.CharField(max_length=100)),
                ('value', models.BigIntegerField()),
                ('balance', models.BigIntegerField()),
                ('date', models.DateField()),
                ('nameRubro', models.BigIntegerField()),
                ('bussines', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Bussines')),
            ],
        ),
        migrations.CreateModel(
            name='Rubro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rubro', models.CharField(max_length=100)),
                ('rubroFather', models.BigIntegerField(null=True)),
                ('nivel', models.IntegerField()),
                ('description', models.TextField()),
                ('dateCreation', models.DateField()),
                ('initialBudget', models.BigIntegerField()),
                ('typeRubro', models.CharField(max_length=100)),
                ('realBudget', models.BigIntegerField()),
                ('budgetEject', models.BigIntegerField()),
                ('imported', models.CharField(max_length=100, null=True)),
                ('bussines', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Bussines')),
                ('inform', models.ManyToManyField(to='budgets.Inform')),
                ('informdetall', models.ManyToManyField(to='budgets.InformDetall')),
                ('origin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Origin')),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codeOp', models.CharField(max_length=2)),
                ('nameOp', models.CharField(max_length=100)),
                ('descriptionOp', models.TextField()),
                ('operation', models.CharField(choices=[('+', '+'), ('-', '-'), ('*', '*'), ('/', '/')], max_length=10)),
                ('orderOp', models.IntegerField()),
                ('contraOperar', models.BigIntegerField(blank=True, null=True)),
                ('contraOperarName', models.CharField(blank=True, max_length=100, null=True)),
                ('contraOrigin', models.BigIntegerField(blank=True, null=True)),
                ('origin', models.ManyToManyField(blank=True, to='budgets.Origin')),
            ],
        ),
        migrations.AddField(
            model_name='movement',
            name='origin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Origin'),
        ),
        migrations.CreateModel(
            name='InformBankDetall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codeInfD', models.CharField(max_length=100)),
                ('descriptionInfD', models.TextField()),
                ('activity', models.CharField(max_length=100)),
                ('inform', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.InformBank')),
            ],
        ),
        migrations.CreateModel(
            name='InformationMovement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeMovement', models.CharField(max_length=100)),
                ('RightsEconomic', models.BooleanField()),
                ('movement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Movement')),
                ('third', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Third')),
            ],
        ),
        migrations.AddField(
            model_name='agreement',
            name='origin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Origin'),
        ),
        migrations.AddField(
            model_name='agreement',
            name='typeAgreement',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.TypeAgreement'),
        ),
        migrations.AddField(
            model_name='accounttyperubro',
            name='bussines',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Bussines'),
        ),
        migrations.AddField(
            model_name='accounttyperubro',
            name='rubro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Rubro'),
        ),
        migrations.AddField(
            model_name='accountperiod',
            name='bussines',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.Bussines'),
        ),
        migrations.AddField(
            model_name='account',
            name='accountPeriod',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.AccountPeriod'),
        ),
    ]
