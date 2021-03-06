from django.shortcuts import render
from apps.budgets.models import *
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from apps.settingsSICAP.forms import *
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.budgets.forms import *
import simplejson as json

# Create your views here.
######################################## Vistas relacionadas con las configuraciones de periodos contable ################################################
class ListAccountPeriod(ListView):


    model = AccountPeriod
    queryset= model.objects.order_by('name')
    template_name = 'settings/mainCreation.html'

    def get_context_data(self):
        context = super(ListAccountPeriod, self).get_context_data()
        context['OriginformS'] = OriginFormSetting
        context['Operationform'] = OperationForm
        context['ACform'] = AccountPeriodForm
        context['ByAccountUpdate'] = ByAccountUpdate
        context['ByBudgetOriginform'] = ByBudgetOriginForm
        return context  

    def get_queryset(self):
        queryset = super(ListAccountPeriod, self).get_queryset()
        return AccountPeriod.objects.filter(bussines_id=self.kwargs['pk'])

class ListOperations(LoginRequiredMixin, ListView):


    login_url = '/login/'
    redirect_field_name = '/login/'
    model = Operation
    queryset= model.objects.order_by('nameOp')
    template_name = 'settings/listOperations.html'

    def get_context_data(self):
        context = super(ListOperations, self).get_context_data()
        context['ContraOperationForm'] = ContraOperationForm
        context['OperationUpdateForm'] = OperationUpdateForm
        return context  

    def get_queryset(self):
        queryset = super(ListOperations, self).get_queryset()
        return Operation.objects.filter(origin=self.kwargs['pk'])

class UpdateAccountPeriod(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def  get(self, request):

        updateAC = AccountPeriod.objects.get(id=request.GET.get('id'))

        
        if request.GET.get('equalName') == 'TRUE':
    
            updateAC.name = request.GET.get('name').upper()
            updateAC.state = request.GET.get('state').upper()
            updateAC.initialDate = request.GET.get('initialDate')
            updateAC.finalDate = request.GET.get('finalDate')
            updateAC.save()
            return JsonResponse({'CREATE':"TRUE"})
        else:
            accountPeriodExist = AccountPeriod.objects.filter(name=request.GET.get('name').upper(),bussines_id=request.GET.get('bussinesId')).exists()
            if accountPeriodExist == False:
                updateAC.name = request.GET.get('name').upper()
                updateAC.state = request.GET.get('state').upper()
                updateAC.initialDate = request.GET.get('initialDate')
                updateAC.finalDate = request.GET.get('finalDate')
                updateAC.save()
                return JsonResponse({'CREATE':"TRUE"})
            else:
                return JsonResponse({'CREATE':"FALSE"}) 
        
class CreateOriginSettings(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def  get(self, request, *args, **kwargs):

        accountPeriod = AccountPeriod.objects.get(id=request.GET.get('accountPeriod'))
        originExist = Origin.objects.filter(nameOrigin=request.GET.get('nameOrigin').upper(), accountPeriod_id=accountPeriod.id).exists()
        if originExist == False:
            nameOrigin = request.GET.get('nameOrigin')
            codeOrigin = request.GET.get('codeOrigin')
            descriptionOrigin = request.GET.get('descriptionOrigin') 
            newOrigin = Origin.objects.create(nameOrigin=nameOrigin.upper(),codeOrigin=codeOrigin.upper(),descriptionOrigin=descriptionOrigin.upper(),orderOrigin=request.GET.get('orderOrigin'),finalDateOrigin=request.GET.get('finalDateOrigin'),accountPeriod=accountPeriod)
            origin = {'id':newOrigin.id,'name':newOrigin.nameOrigin}
            return JsonResponse({'CREATE':"TRUE"})
        else:
            return JsonResponse({'CREATE':"FALSE"})

class GetOriginOperation(LoginRequiredMixin,  View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        originsOperation = Origin.objects.filter(accountPeriod_id=request.GET.get('accountPeriod')).values('nameOrigin')
        return JsonResponse({"OR": list(originsOperation)})
 
class GetOriginSettings(LoginRequiredMixin,  View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        origins = Origin.objects.filter(accountPeriod_id=request.GET.get('accountPeriod')).values('nameOrigin')
        return JsonResponse({"OR": list(origins)})


class CreateOperationSettings(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        origins = json.loads(request.GET.get('origin'))
        for x in range(0,len(origins)):
            getOrigin  = Origin.objects.get(nameOrigin=origins[x], accountPeriod_id=request.GET.get('accountPeriod'))
            objOrigin = Origin.objects.filter(nameOrigin=origins[x], accountPeriod_id=request.GET.get('accountPeriod'))
            operationExist = Operation.objects.filter(nameOp=request.GET.get('nameOp').upper(), origin=getOrigin).exists()
            if operationExist == False:
                newOperation = Operation.objects.create(
                    codeOp=request.GET.get('codeOp').upper(), 
                    nameOp=request.GET.get('nameOp').upper(), 
                    descriptionOp=request.GET.get('descriptionOp').upper(), 
                    operation=request.GET.get('operation').upper(), 
                    orderOp=request.GET.get('orderOp')
                )
                newOperation.origin.add(*objOrigin)
                return JsonResponse({'CREATE':"TRUE"})
            else:
                return JsonResponse({'CREATE':"FALSE"})

class UpdateOperation(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def  get(self, request):
        print('hola actualice operación')
        print(request.GET.get('codeOp'))
        print(request.GET.get('nameOp'))
        print(request.GET.get('descriptionOp'))
        print(request.GET.get('operation'))
        print(request.GET.get('orderOp'))

        
        updateOperation = Operation.objects.get(id=request.GET.get('id'))
        print(request.GET.get('id'))

        if request.GET.get('equalName') == 'TRUE':
    
            updateOperation.codeOp = request.GET.get('codeOp').upper()
            updateOperation.descriptionOp = request.GET.get('descriptionOp').upper()
            updateOperation.operation = request.GET.get('operation').upper()
            updateOperation.orderOp = request.GET.get('orderOp')
            updateOperation.save() 

            return JsonResponse({'CREATE':"TRUE"})
        else:
            operationExist = Operation.objects.filter(nameOp=request.GET.get('nameOp').upper(),bussines_id=request.GET.get('bussinesId')).exists()
            if operationExist == False:

                updateOperation.codeOp = request.GET.get('codeOp').upper()
                updateOperation.nameOp = request.GET.get('nameOp').upper()
                updateOperation.descriptionOp = request.GET.get('descriptionOp').upper()
                updateOperation.operation = request.GET.get('operation')
                updateOperation.orderOp = request.GET.get('orderOp')
                updateOperation.save()

                return JsonResponse({'CREATE':"TRUE"})
            else:
                return JsonResponse({'CREATE':"FALSE"})

class CreateInform(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
      
        nameI=request.GET.get('nameI')
        bussinesId= request.GET.get('bussines')
        bussines = Bussines.objects.get(id=bussinesId)
        InformExist = Inform.objects.filter(nameI=nameI.upper(), bussines_id=bussinesId).exists()
        if InformExist == False:
            newTypeAgreement = Inform.objects.create(
            bussines= bussines,           
            nameI=nameI.upper(), 
            category=request.GET.get('category').upper(), 
            digitI=request.GET.get('digitI')
        )
            return JsonResponse({'CREATE':"TRUE"})
        else:
            return JsonResponse({'CREATE':"FALSE"})  
       

class CreateInformDetall(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        codeInfD=request.GET.get('codeInfD')
        inform = Inform.objects.get(id=request.GET.get('informId'))
        informDetailExist = InformDetall.objects.filter(codeInfD=codeInfD.upper(), inform_id=inform.id).exists()
        if informDetailExist == False:
            newInformDetall = InformDetall.objects.create(
            inform= inform, 
            codeInfD=codeInfD.upper(), 
            descriptionInfD=request.GET.get('descriptionInfD').upper(), 
            activity=request.GET.get('activity').upper()    
        )
            detalle= {'id':newInformDetall.id,'codeInfD':newInformDetall.codeInfD}
            return JsonResponse({'CREATE':"TRUE"})
        else:
            return JsonResponse({'CREATE':"FALSE"})
        
        

class ListInform(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = '/login/'
    model = Inform
    queryset= model.objects.order_by('name')
    template_name = 'settings/listInform.html'

    def get_context_data(self):
        context = super(ListInform, self).get_context_data()
        context['InformFormDetall'] = InformFormDetall
        context['InformForm'] = InformForm
        context['ByInformUpdate'] = ByInformUpdate

        return context  

    def get_queryset(self):
        queryset = super(ListInform, self).get_queryset()
        return Inform.objects.filter(bussines_id=self.kwargs['pk'])

class UpdateInform(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def  get(self, request):
        
        updateInforme = Inform.objects.get(id=request.GET.get('id'))
        nameI=request.GET.get('nameI').upper()
        if request.GET.get('equalName') == 'TRUE':
    
            updateInforme.category = request.GET.get('category').upper()
            updateInforme.digitI = request.GET.get('digitI')
            updateInforme.save() 
            return JsonResponse({'CREATE':"TRUE"})
        else:
            informExist = Inform.objects.filter(nameI=request.GET.get('nameI').upper(),bussines_id=request.GET.get('bussinesId')).exists()
            if informExist == False:
                updateInforme.nameI = nameI
                updateInforme.category = request.GET.get('category').upper()
                updateInforme.digitI = request.GET.get('digitI')
                updateInforme.save() 
                return JsonResponse({'CREATE':"TRUE"})
            else:
                return JsonResponse({'CREATE':"FALSE"})   


class CreateTypeAgreement(LoginRequiredMixin, View):
    
    login_url = '/login/'
    redirect_field_name = '/login/'
    def get(self, request, *args, **kwargs):

        nameTA=request.GET.get('nameTA')
        bussinesId= request.GET.get('bussines')
        bussines = Bussines.objects.get(id=bussinesId)
        typeAgreementExist = TypeAgreement.objects.filter(nameTA=nameTA.upper(), bussines_id=bussinesId).exists()
        if typeAgreementExist == False:
            newTypeAgreement = TypeAgreement.objects.create(
            bussines= bussines,           
            codeTA=request.GET.get('codeTA').upper(), 
            nameTA=nameTA.upper(), 
            descriptionTA=request.GET.get('descriptionTA').upper(), 
            ordenTA=request.GET.get('ordenTA')
        )
            return JsonResponse({'CREATE':"TRUE"})
        else:
            return JsonResponse({'CREATE':"FALSE"})
        
            

class ListTypeAgreement(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = '/login/'
    model = TypeAgreement
    queryset= model.objects.order_by('nameTA')
    template_name = 'settings/listTypeAgreement.html'

    def get_context_data(self):
        context = super(ListTypeAgreement, self).get_context_data()
        context['TypeAgreementForm'] = TypeAgreementForm
        context['ByTypeAgreementUpdate'] = ByTypeAgreementUpdate

        return context  

    def get_queryset(self):
        queryset = super(ListTypeAgreement, self).get_queryset()
        return TypeAgreement.objects.filter(bussines_id=self.kwargs['pk'])
        
class UpdateTipeAgreement(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def  get(self, request):

        updateTypeAgreement = TypeAgreement.objects.get(id=request.GET.get('id'))
        codeTA=request.GET.get('codeTA').upper()
        if request.GET.get('equalCode') == 'TRUE':
    
            updateTypeAgreement.codeTA = codeTA.upper()
            updateTypeAgreement.nameTA = request.GET.get('nameTA').upper()
            updateTypeAgreement.descriptionTA = request.GET.get('descriptionTA').upper()
            updateTypeAgreement.ordenTA = request.GET.get('ordenTA')
            updateTypeAgreement.save()     
            return JsonResponse({'CREATE':"TRUE"})
        else:
            tipeAgreementExist = TypeAgreement.objects.filter(codeTA=codeTA, bussines_id=request.GET.get('bussinesId')).exists()
            if tipeAgreementExist == False:
                updateTypeAgreement.codeTA = codeTA.upper()
                updateTypeAgreement.nameTA = request.GET.get('nameTA').upper()
                updateTypeAgreement.descriptionTA = request.GET.get('descriptionTA').upper()
                updateTypeAgreement.ordenTA = request.GET.get('ordenTA')
                updateTypeAgreement.save()   
                return JsonResponse({'CREATE':"TRUE"})
            else:
                return JsonResponse({'CREATE':"FALSE"}) 


class DeleteAll(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def get(self, request, *args, **kwargs):

        option = request.GET.get('option')
        if option=='1':

            accountPeriod = AccountPeriod.objects.get(id=request.GET.get('id'))
            accountPeriod.delete()
            return JsonResponse({'Eliminado': 'True'})
        elif option=='2':

            inform = Inform.objects.get(id=request.GET.get('id'))
            inform.delete()
            return JsonResponse({'Eliminado': 'True'})
        elif option=='3':
            typeAgreement = TypeAgreement.objects.get(id=request.GET.get('id'))
            typeAgreement.delete()
            return JsonResponse({'Eliminado': 'True'})
        elif option=='4':
            voucher = Voucher.objects.get(id=request.GET.get('id'))
            voucher.delete()
            return JsonResponse({'Eliminado': 'True'})
        elif option=='5':
            third = Third.objects.get(id=request.GET.get('id'))
            third.delete()
            return JsonResponse({'Eliminado': 'True'})
        elif option=='6':
            typeContract = TypeContract.objects.get(id=request.GET.get('id'))
            typeContract.delete()
            return JsonResponse({'Eliminado': 'True'})
        else:
            operation = Operation.objects.get(id=request.GET.get('id'))
            operation.delete()
            return JsonResponse({'Eliminado': 'True'})

class GetOperationsContra(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def get(self, request, *args, **kwargs):

        origin= Origin.objects.filter(nameOrigin=request.GET.get('nameOrigin'), accountPeriod_id=request.GET.get('accountID')).values('id')
        operations = Operation.objects.filter(origin=origin[0]['id']).values('nameOp')
        return JsonResponse({'OP': list(operations)})

class UpdateContraOperation(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        currentOperation = Operation.objects.get(id=request.GET.get('operation'))
        origin= Origin.objects.get(nameOrigin=request.GET.get('nameOrigin'), accountPeriod_id=request.GET.get('accountID'))
        idContrOperation = Operation.objects.get(origin=origin.id,nameOp=request.GET.get('nameOp'))
        currentOperation.contraOperar = idContrOperation.id
        currentOperation.contraOrigin = origin.id
        currentOperation.save()
        return JsonResponse({'TRUE': 'OK'})

class ChangeWindowsOperation(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        origin = Origin.objects.get(nameOrigin=request.GET.get('origin')[:-1],accountPeriod_id=request.GET.get('accountPeriod'))
        return JsonResponse({'TRUE': 'OK', 'OR': origin.id})

