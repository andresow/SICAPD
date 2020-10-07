from django import forms
from apps.budgets.models import *
from django.forms.fields import DateField

class OriginFormSetting(forms.ModelForm):
        

    class Meta:
        model = Origin
        fields = [
                'codeOrigin',
                'nameOrigin',
                'descriptionOrigin',
                'orderOrigin',
                'finalDateOrigin',
                             
        ]
        
        labels = {
                'codeOrigin': 'Código',
                'nameOrigin': 'Nombre',
                'descriptionOrigin': 'Descripción',    
                'orderOrigin': 'Orden',
                'finalDateOrigin': 'Fecha final',
                
        }

        widgets = { 				

                'Código':forms.TextInput(),
                'Nombre':forms.TextInput(),
                'Descripción':forms.TextInput(),
                'Orden':forms.TextInput(),
                'Fecha final':forms.DateInput(format=('%d-%m-%Y'),attrs={'class':'myDateClass','placeholder':'Select a date'}),
                
        }

class TypeAgreementForm(forms.ModelForm):
        

    class Meta:
        model = TypeAgreement
        fields = [
                'codeTA',
                'nameTA',
                'descriptionTA',
                'ordenTA',
        ]
        
        labels = {
                'codeTA': 'Código',
                'nameTA': 'Nombre',
                'descriptionTA': 'Descripción',
                'ordenTA': 'Orden',                
        }

        widgets = { 				
                'Código':forms.TextInput(),
                'Nombre':forms.TextInput(),
                'Descripción':forms.TextInput(),
                'Orden':forms.TextInput(),                
        }


class InformForm(forms.ModelForm):
        

    class Meta:
        model = Inform
        fields = [
                'nameI',
                'category',
                'digitI',
        ]
        
        labels = {
                'nameI': 'Nombre',
                'category': 'Categoría',
                'digitI': 'Dígito',                
        }

        widgets = { 				
                'Nombre':forms.TextInput(),
                'Categoría':forms.TextInput(),
                'Dígito':forms.TextInput(),                
        }


class InformFormDetall(forms.ModelForm):
        

    class Meta:
        model = InformDetall
        fields = [
                'codeInfD',
                'descriptionInfD',
                'activity',
        ]
        
        labels = {
                'codeInfD': 'Código',
                'descriptionInfD': 'Descripción de detalles',
                'activity': 'Actividad',
        }

        widgets = { 				
                'Código':forms.TextInput(),
                'Descripción de detalles':forms.TextInput(),
                'Actividad':forms.TextInput(),
        }

class ByAccountUpdate(forms.Form):

        CHOICES = [('Activo','Activo'),('Inactivo', 'Inactivo')]

        nameUpdate = forms.CharField()
        stateUpdate = forms.ChoiceField(choices=CHOICES)
        initialDateUAC = forms.DateField()
        finalDatenUAC = forms.DateField()

        def __init__(self, *args, **kwargs):
                super(ByAccountUpdate, self).__init__(*args, **kwargs)
                
                self.fields['nameUpdate'].label = 'Nombre'
                self.fields['stateUpdate'].label = 'Estado'
                self.fields['initialDateUAC'].label = 'Fecha inicial'
                self.fields['finalDatenUAC'].label = 'Fecha final'

class ByInformUpdate(forms.Form):

        nameIUpdate = forms.CharField()
        categoryUpdate = forms.CharField()          
        digitIUpdate= forms.CharField()
        
        def __init__(self, *args, **kwargs):
                super(ByInformUpdate, self).__init__(*args, **kwargs)
                
                self.fields['nameIUpdate'].label = 'Nombre'
                self.fields['categoryUpdate'].label = 'Categoría'
                self.fields['digitIUpdate'].label = 'Dígito'

class ByTypeAgreementUpdate(forms.Form):

        codeTAUpdate = forms.CharField()
        nameTAUpdate = forms.CharField()
        descriptionTAUpdate = forms.CharField()          
        ordenTAUpdate= forms.CharField()
        
        def __init__(self, *args, **kwargs):
                super(ByTypeAgreementUpdate, self).__init__(*args, **kwargs)
                
                self.fields['codeTAUpdate'].label = 'Código'
                self.fields['nameTAUpdate'].label = 'Nombre'
                self.fields['descriptionTAUpdate'].label = 'Descripción'
                self.fields['ordenTAUpdate'].label = 'Orden'

class ContraOperationForm(forms.Form):

        origen = forms.ChoiceField()
        contraoperation = forms.ChoiceField()
        
        def __init__(self, *args, **kwargs):
                super(ContraOperationForm, self).__init__(*args, **kwargs)
                
                self.fields['origen'].label = 'Seleccione su origen'
                self.fields['contraoperation'].label = 'Seleccione su contraoperación'

class OperationUpdateForm(forms.Form):

        CHOICES = [('+','+'),('-', '-'),('*', '*'),('/', '/')]
        codeOpUpdate = forms.CharField()
        nameOpUpdate = forms.CharField()
        operationOpUpdate = forms.ChoiceField(choices=CHOICES)
        orderOpUpdate = forms.CharField()
    
        def __init__(self, *args, **kwargs):
                super(OperationUpdateForm, self).__init__(*args, **kwargs)
        
                self.fields['codeOpUpdate'].label = 'Código'
                self.fields['nameOpUpdate'].label = 'Nombre'
                self.fields['operationOpUpdate'].label = 'Operación'
                self.fields['orderOpUpdate'].label = 'Orden'
                
class ByBudgetOriginForm(forms.Form):

        originSelectO = forms.ChoiceField()

        def __init__(self, *args, **kwargs):
                super(ByBudgetOriginForm, self).__init__(*args, **kwargs)
                
                self.fields['originSelectO'].label = 'Seleccione el origen'