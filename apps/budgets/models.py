from django.db import models
from django.forms.fields import DateField
class Bussines(models.Model):

    # user = models.ForeignKey(Nodes, null=True, blank=True, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, unique=True)
    nit = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    address =  models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    representative = models.CharField(max_length=100)
    rubroPattern = models.CharField(max_length=100)
    accountPattern = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.name)

class AccountPeriod(models.Model):

    CHOICES = [('Activo','Activo'),('Inactivo', 'Inactivo')]
    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100,choices=CHOICES)
    initialDate = models.DateField()
    finalDate = models.DateField()

    def __str__(self):
        return '{}'.format(self.name)

class Origin(models.Model):
    
    # Opcional poner la empresa
    # bussines = models.ForeignKey(Bussines, null=False, blank=True, on_delete=models.CASCADE)
    accountPeriod = models.ForeignKey(AccountPeriod, null=False, blank=True, on_delete=models.CASCADE)
    nameOrigin = models.CharField(max_length=100)
    codeOrigin = models.CharField(max_length=100)
    descriptionOrigin = models.TextField()
    orderOrigin = models.IntegerField()
    finalDateOrigin = models.DateField()

    def __str__(self):
        return '{}'.format(self.nameOrigin)

class Operation(models.Model):

    CHOICES = [('+','+'),('-', '-'),('*', '*'),('/', '/')]

    origin = models.ManyToManyField(Origin, blank=True)
    codeOp = models.CharField(max_length=2)
    nameOp = models.CharField(max_length=100)
    descriptionOp = models.TextField()
    operation = models.CharField(max_length=10,choices=CHOICES)
    orderOp = models.IntegerField()
    contraOperar = models.BigIntegerField(null=True, blank=True)
    contraOperarName = models.CharField(max_length=100,null=True, blank=True)
    contraOrigin = models.BigIntegerField(null=True, blank=True) 

    # Opcional poner  el periodo por facilidad
    # accountPeriod = models.ForeignKey(AccountPeriod, null=False, blank=True, on_delete=models.CASCADE)

class TypeAgreement(models.Model):

    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    codeTA = models.CharField(max_length=100) 
    nameTA = models.CharField(max_length=100) 
    descriptionTA = models.TextField()
    ordenTA =  models.IntegerField()
    validacionTA = models.CharField(max_length=100, blank=True)
    mensajeTA = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return '{}'.format(self.nameTA)

class Agreement(models.Model):

    origin = models.ForeignKey(Origin, null=True, blank=True, on_delete=models.CASCADE)
    numberAg = models.CharField(max_length=100)
    descriptionAg = models.TextField() 
    dateAg  = models.DateField()
    typeAgreement = models.ForeignKey(TypeAgreement, null=False, blank=True, on_delete=models.CASCADE)

class Inform(models.Model):

    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    nameI = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    digitI = models.BigIntegerField()

class InformDetall(models.Model):

    inform = models.ForeignKey(Inform, null=True, blank=True, on_delete=models.CASCADE)
    codeInfD = models.CharField(max_length=100)
    descriptionInfD = models.TextField() 
    activity = models.CharField(max_length=100)

class Rubro(models.Model):

    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    origin =  models.ForeignKey(Origin, null=True, blank=True, on_delete=models.CASCADE)
    rubro = models.CharField(max_length=100)
    rubroFather = models.BigIntegerField(null=True)
    nivel = models.IntegerField()
    description = models.TextField() 
    dateCreation = models.DateField()
    initialBudget = models.BigIntegerField()
    typeRubro = models.CharField(max_length=100)
    inform = models.ManyToManyField(Inform)
    informdetall = models.ManyToManyField(InformDetall)
    realBudget = models.BigIntegerField()
    budgetEject = models.BigIntegerField()
    imported =  models.CharField(max_length=100, null=True)

class Movement(models.Model):

    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    agreement = models.ForeignKey(Agreement, null=True, blank=True, on_delete=models.CASCADE)
    nameRubro =  models.BigIntegerField(null=True)
    concept = models.CharField(max_length=100)
    value = models.BigIntegerField()
    balance = models.BigIntegerField()
    date = models.DateField()
    disponibility = models.BigIntegerField(null=True)
    register = models.BigIntegerField(null=True)
    obligation = models.BigIntegerField(null=True)
    origin =  models.ForeignKey(Origin, null=True, blank=True, on_delete=models.CASCADE)
    observation = models.TextField(null=True)

class RubroMovement(models.Model):

    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    value = models.BigIntegerField()
    valueP =  models.BigIntegerField()
    balance = models.BigIntegerField()
    date = models.DateField()
    nameRubro =  models.BigIntegerField()
    movement = models.ForeignKey(Movement, null=True, blank=True, on_delete=models.CASCADE)

class RubroBalanceOperation(models.Model):

    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    typeOperation = models.CharField(max_length=100)
    value =  models.BigIntegerField()
    balance = models.BigIntegerField()
    date = models.DateField()
    nameRubro =  models.BigIntegerField()

class Voucher(models.Model):

    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    name =  models.CharField(max_length=100)
    description = models.TextField()
    order =  models.IntegerField()
    number =  models.IntegerField()
    category = models.CharField(max_length=100)
    dateCreation = models.DateField()

class Third(models.Model):
    
    CHOICES = [('Cédula de Ciudadanía', 'Cédula de Ciudadanía'), ('Cédula Extranjeria', 'Cédula Extrangeria'), ('Pasaporte', 'Pasaporte')]
    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    typeIdentification = models.CharField(max_length=64, choices=CHOICES)
    identification = models.BigIntegerField()
    name =  models.CharField(max_length=100)
    surnames = models.CharField(max_length=100)
    reason =  models.CharField(max_length=100)
    phone =  models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    
class TypeContract(models.Model):

    bussines = models.ForeignKey(Bussines, null=True, blank=True, on_delete=models.CASCADE)
    nameTC = models.CharField(max_length=100)
    description = models.TextField()
    categoryTC = models.CharField(max_length=100)
    digitsTC = models.BigIntegerField()

class TypeContractDetail(models.Model):

    typeContract = models.ForeignKey(TypeContract, null=True, blank=True, on_delete=models.CASCADE)
    codeTypeC = models.CharField(max_length=100)
    descriptionTypeC = models.TextField() 
    activity = models.CharField(max_length=100)

