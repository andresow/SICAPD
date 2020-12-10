from django.shortcuts import render
from apps.budgets.models import *
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from apps.settingsSICAP.forms import *
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.budgets.forms import *
import simplejson as json
from django.db.models import Count


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
    def  get(self, request, *args, **kwargs): 

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
        print("entre eeee")
        print(self.kwargs['pkUser'])
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
    def  get(self, request, *args, **kwargs):
        print('hola entre')
        print(request.GET.get('codeOp'))
        print(request.GET.get('nameOp'))
        print(request.GET.get('operation'))
        print(request.GET.get('orderOp')) 
        
        updateOperation = Operation.objects.get(id=request.GET.get('id'))
        nameOp = request.GET.get('nameOp').upper()
        if request.GET.get('equalName') == 'TRUE':
    
            updateOperation.codeOp = request.GET.get('codeOp').upper()
            updateOperation.operation = request.GET.get('operation')
            updateOperation.orderOp = request.GET.get('orderOp')
            updateOperation.save() 
            return JsonResponse({'CREATE':"TRUE"})
        else:
            operationExist = Operation.objects.filter(nameOp=request.GET.get('nameOp').upper(),bussines_id=request.GET.get('bussinesId')).exists()
            if operationExist == False:
                updateOperation.codeOp = request.GET.get('codeOp').upper()
                updateOperation.nameOp = nameOp
                updateOperation.operation = request.GET.get('operation')
                updateOperation.orderOp = request.GET.get('orderOp')
                updateOperation.save() 
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
        
class UpdateInform(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def  get(self, request, *args, **kwargs): 
        
        updateInforme = Inform.objects.get(id=request.GET.get('id'))
        nameI = request.GET.get('nameI').upper()
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
    def  get(self, request, *args, **kwargs): 

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
        elif option=='7':
            operation = Operation.objects.get(id=request.GET.get('id'))
            operation.delete()
            return JsonResponse({'Eliminado': 'True'})
        elif option=='8':
            agreement = Agreement.objects.get(id=request.GET.get('id'))
            agreement.delete()
            listAgreement = Agreement.objects.filter(origin_id=request.GET.get('origin')).values('id', 'typeAgreement', 'numberAg', 'descriptionAg')
            return JsonResponse({'Eliminado': 'True', 'AG':list(listAgreement)})
        elif option=='9':
            movementExist = Movement.objects.filter(disponibility=request.GET.get('id')).exists()
            if movementExist == True:
                return JsonResponse({'Eliminado': 'False'})
            else:
                movement = Movement.objects.get(id=request.GET.get('id'))
                rubros = RubroMovement.objects.filter(movement_id=request.GET.get('id')).values('nameRubro','value')
                for x in range(0,len(rubros)):
                    rubro = Rubro.objects.get(id=rubros[x]['nameRubro'])
                    rubro.budgetEject = rubro.budgetEject + rubros[x]['value']
                    rubro.save()
                movement.delete()
                listMovement = Movement.objects.filter(origin_id=request.GET.get('origin'),concept="DISPONIBILIDAD").values('id','date','value','balance','disponibility','observation')
                return JsonResponse({'Eliminado': 'True', 'MV':list(listMovement)})
        elif option=='10':
            registerExist = Movement.objects.filter(register=request.GET.get('id')).exists()
            if registerExist == True:
                return JsonResponse({'Eliminado': 'False'})
            else:
                register = Movement.objects.get(id=request.GET.get('id'))         
                rubros = RubroMovement.objects.filter(movement_id=request.GET.get('id')).values('nameRubro','value')
                for x in range(0,len(rubros)):
                    rubrosDisponibility = RubroMovement.objects.get(movement_id=register.disponibility, nameRubro=rubros[x]['nameRubro']) 
                    rubrosDisponibility.valueP =  rubrosDisponibility.valueP+ rubros[x]['value'] 
                    rubrosDisponibility.save()
                register.delete()
                listRegister = Movement.objects.filter(origin_id=request.GET.get('origin'),concept="REGISTRO").values('id','date','value','balance','register','observation')
                return JsonResponse({'Eliminado': 'True', 'RG':list(listRegister)})
        elif option=='11':
            obligationExist = Movement.objects.filter(obligation=request.GET.get('id')).exists()
            if obligationExist == True:
                return JsonResponse({'Eliminado': 'False'})
            else:
                obligation = Movement.objects.get(id=request.GET.get('id'))
                rubros = RubroMovement.objects.filter(movement_id=request.GET.get('id')).values('nameRubro','value')
                for x in range(0,len(rubros)):
                    rubrosRegister = RubroMovement.objects.get(movement_id=obligation.register, nameRubro=rubros[x]['nameRubro']) 
                    rubrosRegister.valueP =  rubrosRegister.valueP+ rubros[x]['value'] 
                    rubrosRegister.save()
                obligation.delete()
                listObligation = Movement.objects.filter(origin_id=request.GET.get('origin'),concept="OBLIGACION").values('id','date','value','balance','obligation','observation')
                return JsonResponse({'Eliminado': 'True', 'OB':list(listObligation)})
        elif option=='12':
            disponibility = Movement.objects.get(id=request.GET.get('disponibility'))  
            rubro = Rubro.objects.get(id=request.GET.get('id'))
            rubroDispo = RubroMovement.objects.get(id=request.GET.get('dispoID'))
            rubro.budgetEject = rubro.budgetEject + int(request.GET.get('budgetEject'))
            disponibility.balance = disponibility.balance - rubroDispo.balance
            disponibility.value = disponibility.value - rubroDispo.value
            rubro.save()  
            disponibility.save()
            rubroDispo.delete()
            rubroMov = RubroMovement.objects.filter(movement_id=request.GET.get('disponibility')).values('id','nameRubro','value','balance','valueP')
            rubroList = []

            for x in range(0,len(list(rubroMov))):
                rubro = Rubro.objects.get(id=list(rubroMov)[x]['nameRubro'])
                rubroList.append({"dispoID":list(rubroMov)[x]['id'],"id":rubro.id,"rubro":rubro.rubro,"description":rubro.description,"realBudget":rubro.realBudget ,"value":list(rubroMov)[x]['value'],"balance":list(rubroMov)[x]['balance'],"budgetEject":list(rubroMov)[x]['valueP']})

            if len(list(rubroMov)) == 0:
                disponibility.delete()
                listMovement = Movement.objects.filter(origin_id=request.GET.get('origin'),concept="DISPONIBILIDAD").values('id','date','value','balance','disponibility','observation')
                return JsonResponse({"RUBRO": list(rubroList),"MV": list(listMovement)})
            else:    
                listMovement = Movement.objects.filter(origin_id=request.GET.get('origin'),concept="DISPONIBILIDAD").values('id','date','value','balance','disponibility','observation')
                return JsonResponse({"RUBRO": list(rubroList),"MV": list(listMovement)})
        elif option=='13':
            disponibility = Movement.objects.get(id=request.GET.get('disponibility'))            
            return JsonResponse({"RUBRO": list(rubroList)})
        elif option=='14':
            deleteAccount = Account.objects.get(id=request.GET.get('id'))
            accountExists = valueAccountObligation.objects.filter(accountRubro__account_id=request.GET.get('id')).exists()
            if accountExists == False:
                deleteAccount.delete()
                return JsonResponse({'ELIMINADO': 'TRUE'})
            else:
                return JsonResponse({"ELIMINADO": 'FALSE'})
            
        elif option=='15':
            informBank = InformBank.objects.get(id=request.GET.get('id'))
            informBank.delete()
            return JsonResponse({'Eliminado': 'True'})
        elif option=='16':
            register = Movement.objects.get(id=request.GET.get('registerID'))  
            rubroRegister = RubroMovement.objects.get(id=request.GET.get('id'))
            register.value = register.value - rubroRegister.value
            register.balance = register.balance - rubroRegister.balance
            register.save()  
            rubroMov = RubroMovement.objects.filter(movement_id=request.GET.get('registerID')).values('id','nameRubro','value','balance','valueP')
            rubroList = []
            disponibility =  RubroMovement.objects.get(movement_id=register.disponibility,nameRubro=rubroRegister.nameRubro)
            disponibility.valueP =  int(disponibility.valueP) + int(rubroRegister.value)
            disponibility.save()  
            rubroRegister.delete()

            for x in range(0,len(list(rubroMov))):
                rubro = Rubro.objects.get(id=list(rubroMov)[x]['nameRubro'])
                rubroList.append({"registerID":list(rubroMov)[x]['id'],"id":rubro.id,"rubro":rubro.rubro,"description":rubro.description,"realBudget":rubro.realBudget ,"value":list(rubroMov)[x]['value'],"balance":list(rubroMov)[x]['balance'],"budgetEject":list(rubroMov)[x]['valueP']})
            
            if len(list(rubroMov)) == 0:
                register.delete()
                listRegister = Movement.objects.filter(origin_id=request.GET.get('origin'),concept="REGISTRO").values('id','date','value','balance','register','observation')
                return JsonResponse({"DRG": list(rubroList),"RG": list(listRegister)})
            else:    
                listRegister = Movement.objects.filter(origin_id=request.GET.get('origin'),concept="REGISTRO").values('id','date','value','balance','register','observation')
                return JsonResponse({"DRG": list(rubroList),"RG": list(listRegister)})   
        else:
            obligation = Movement.objects.get(id=request.GET.get('obligationID'))  
            rubroObligation = RubroMovement.objects.get(id=request.GET.get('id'))
            obligation.value = obligation.value - rubroObligation.value
            obligation.balance = obligation.balance - rubroObligation.balance
            obligation.save()  
            rubroMov = RubroMovement.objects.filter(movement_id=request.GET.get('obligationID')).values('id','nameRubro','value','balance','valueP')
            rubroList = []
            register =  RubroMovement.objects.get(movement_id=obligation.register,nameRubro=rubroObligation.nameRubro)
            register.valueP =  int(register.valueP) + int(register.value)
            register.save()  
            rubroObligation.delete()

            for x in range(0,len(list(rubroMov))):
                rubro = Rubro.objects.get(id=list(rubroMov)[x]['nameRubro'])
                rubroList.append({"idObligation":list(rubroMov)[x]['id'],"id":rubro.id,"rubro":rubro.rubro,"description":rubro.description,"realBudget":rubro.realBudget ,"value":list(rubroMov)[x]['value'],"balance":list(rubroMov)[x]['balance'],"budgetEject":list(rubroMov)[x]['valueP']})
            
            if len(list(rubroMov)) == 0:
                obligation.delete()
                listObligation = Movement.objects.filter(origin_id=request.GET.get('origin'),concept="OBLIGACION").values('id','date','value','balance','register','observation')
                return JsonResponse({"OB": list(rubroList),"MV": list(listObligation)})
            else:    
                listObligation = Movement.objects.filter(origin_id=request.GET.get('origin'),concept="OBLIGACION").values('id','date','value','balance','register','observation')
                return JsonResponse({"OB": list(rubroList),"MV": list(listObligation)})  
        

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
        currentOperation.contraOperarName = idContrOperation.nameOp
        currentOperation.save()
        return JsonResponse({'TRUE': 'OK'})

class ChangeWindowsOperation(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        origin = Origin.objects.get(nameOrigin=request.GET.get('origin')[:-1],accountPeriod_id=request.GET.get('accountPeriod'))
        return JsonResponse({'TRUE': 'OK', 'OR': origin.id})


class ListAccount(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = '/login/'
    model = Account
    queryset= model.objects.order_by('name')
    template_name = 'settings/listAccount.html'

    def get_context_data(self):
        context = super(ListAccount, self).get_context_data()
        context['AccountForm'] = AccountForm
        context['AccountUpdate'] = AccountUpdate

        return context  

    def get_queryset(self):
        queryset = super(ListAccount, self).get_queryset()
        return Account.objects.filter(accountPeriod_id=self.kwargs['pk'])

class CreateAccount(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
      
        code=request.GET.get('code')
        accountPeriod = AccountPeriod.objects.get(id=request.GET.get('accountId'))
        AccountExist = Account.objects.filter(code=code.upper(), accountPeriod_id=accountPeriod.id).exists()
        if AccountExist == False:
            if len(request.GET.get('code')) == 1:
                if request.GET.get('typeRubro') == 'A':
                    newAccount = Account.objects.create(accountPeriod_id= accountPeriod.id, code=code.upper(), description=request.GET.get('description').upper(), nature=request.GET.get('nature').upper(),
                    level=request.GET.get('level'),typeAccount='A',corriente=request.GET.get('corriente').upper(),
                    state=request.GET.get('state').upper())
                    return JsonResponse({'CREATE':"TRUE"})
                else:
                    newAccount = Account.objects.create(accountPeriod_id= accountPeriod.id, code=code.upper(), description=request.GET.get('description').upper(), nature=request.GET.get('nature').upper(),
                    level=request.GET.get('level'),typeAccount='M',corriente=request.GET.get('corriente').upper(),
                    state=request.GET.get('state').upper())
                    return JsonResponse({'CREATE':"TRUE"})
            else:
                if request.GET.get('typeRubro') == 'A':
                    newAccount = Account.objects.create(accountPeriod_id= accountPeriod.id, code=code.upper(), description=request.GET.get('description').upper(), nature=request.GET.get('nature').upper(),
                    level=request.GET.get('level'),typeAccount='A',corriente=request.GET.get('corriente').upper(),
                    state=request.GET.get('state').upper(),accountFather=int(request.GET.get('accountFather')))
                    return JsonResponse({'CREATE':"TRUE"})
                else:
                    newAccount = Account.objects.create(accountPeriod_id= accountPeriod.id, code=code.upper(), description=request.GET.get('description').upper(), nature=request.GET.get('nature').upper(),
                    level=request.GET.get('level'),typeAccount='M',corriente=request.GET.get('corriente').upper(),
                    state=request.GET.get('state').upper(),accountFather=int(request.GET.get('accountFather')))
                    return JsonResponse({'CREATE':"TRUE"})
        else:
            return JsonResponse({'CREATE':"FALSE"})  

class UpdateAccount(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def  get(self, request, *args, **kwargs): 
        
        updateAccount = Account.objects.get(id=request.GET.get('id'))
        code=request.GET.get('code').upper()
        if request.GET.get('equalCode') == 'TRUE':
    
            updateAccount.description = request.GET.get('description').upper()
            updateAccount.nature = request.GET.get('nature')
            updateAccount.level = request.GET.get('level')
            updateAccount.save() 
            return JsonResponse({'CREATE':"TRUE"})
        else:
            accountExist = Account.objects.filter(code=request.GET.get('code').upper(),bussines_id=request.GET.get('bussinesId')).exists()
            if accountExist == False:
                updateAccount.code = code
                updateAccount.description = request.GET.get('description').upper()
                updateAccount.nature = request.GET.get('nature')
                updateAccount.level = request.GET.get('level')
                updateAccount.save()  
                return JsonResponse({'CREATE':"TRUE"})
            else:
                return JsonResponse({'CREATE':"FALSE"}) 

def generateAccounting(request,pkUser):

    return render(request, 'settings/generateAccounting.html')

class GetAccountSettings(LoginRequiredMixin,  View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        accounts = Account.objects.filter(accountPeriod_id=request.GET.get('idAC')).values('id', 'code', 'description')
        return JsonResponse({"ACC": list(accounts)})

class CreateAccountingOpTip(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
      
        account=request.GET.get('account')
        bussinesId= request.GET.get('bussines')
        bussines = Bussines.objects.get(id=bussinesId)
        accountingOpExist = Account.objects.filter(account=account.upper(), bussines_id=bussinesId).exists()
        if accountingOpExist == False:
            newAccountingOp = Account.objects.create(
            bussines= bussines,           
            account=account.upper(), 
            operation=request.GET.get('operation').upper(), 
            operationAccount=request.GET.get('operationAccount').upper(),
        )
            return JsonResponse({'CREATE':"TRUE"}) 
        else:
            return JsonResponse({'CREATE':"FALSE"})  


class GetBudget(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        print('función para contar las cuentas agregadas a el rubro')

        nameOrigin = request.GET.get('nameOrigin')
        accountPeriod = AccountPeriod.objects.get(name=request.GET.get('nameAC')[:-1])
        origin = Origin.objects.get(nameOrigin=nameOrigin, accountPeriod=accountPeriod.id)
        rubro = Rubro.objects.filter(origin_id=origin.id, bussines_id=request.GET.get('idBussines')).values('id','rubro','rubroFather','typeRubro','description','dateCreation','initialBudget','realBudget','budgetEject').order_by('rubro')
        listRubroAccount = []
        for x in range(0,len(list(rubro))):

            totalAccounts = AccountTypeRubro.objects.filter(rubro_id=(list(rubro)[x]['id'])).count()
           
            listRubroAccount.append({"id":list(rubro)[x]['id'], "total":totalAccounts})
          
        return JsonResponse({"ID":origin.id ,"RUBRO": list(rubro), "TRA": list(listRubroAccount)})

class CreateAccountRubro(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def post(self, request, *args, **kwargs):

        
        accountRubro = json.loads(request.POST.get('accountRubro'))
        bussines = Bussines.objects.get(id=request.POST.get('bussines'))
        for x in range(0,len(accountRubro)):
             
            rubro = Rubro.objects.get(id=accountRubro[x]['rubro'])
            account = Account.objects.get(id=accountRubro[x]['account'])
            typeAccount = accountRubro[x]['operationAccount']
            document = accountRubro[x]['document']
            accountType = AccountTypeRubro.objects.filter(rubro_id=rubro.id,account_id=account.id,typeAccount=typeAccount).exists()
            if accountType == True:
                return JsonResponse({"CREATE": "FALSE","TA":typeAccount})
            else:
                AccountTypeRubro.objects.create(bussines=bussines,rubro=rubro,account=account,typeAccount=typeAccount,document=document)
        return JsonResponse({"CREATE": "TRUE"})

class GetAccountsByRubro(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        accountsByRubro = AccountTypeRubro.objects.filter(rubro_id=request.GET.get('rubro')).values('id','rubro__id','account__code','account__description','typeAccount','document','account_id','id')        
        print(accountsByRubro)
        return JsonResponse({"AC":list(accountsByRubro)})

class SearchAccount(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        
        accountLen = request.GET.get('account')
        if len(accountLen) == 1:
            return JsonResponse({"ACCOUNTFATHER": "PRIMERA CUENTA"})
        else:  
            accountExists = Account.objects.get(code=request.GET.get('account'),accountPeriod_id=request.GET.get('accountPeriod'))
            return JsonResponse({"ACCOUNTFATHER": "TRUE", "FATHER":accountExists.code, "LEVEL":accountExists.id,"TYPEACCOUNT": accountExists.typeAccount}) 

class ListInformBank(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = '/login/'
    model = InformBank
    queryset= model.objects.order_by('name')
    template_name = 'settings/listInformBank.html'

    def get_context_data(self):
        context = super(ListInformBank, self).get_context_data()

        context['InformBankForm'] = InformForm
        context['InformDetailBankForm'] = InformFormDetall
        context['ByInformBankUpdateForm'] = ByInformUpdate

        return context  

    def get_queryset(self):
        queryset = super(ListInformBank, self).get_queryset()
        return InformBank.objects.filter(bussines_id=self.kwargs['pk'])

class CreateInformBank(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
      
        nameI=request.GET.get('nameI')
        bussinesId= request.GET.get('bussines')
        bussines = Bussines.objects.get(id=bussinesId)
        InformExist = InformBank.objects.filter(nameI=nameI.upper(), bussines_id=bussinesId).exists()
        if InformExist == False:
            newTypeAgreement = InformBank.objects.create(
            bussines= bussines,           
            nameI=nameI.upper(), 
            category=request.GET.get('category').upper(), 
            digitI=request.GET.get('digitI')
        )
            return JsonResponse({'CREATE':"TRUE"})
        else:
            return JsonResponse({'CREATE':"FALSE"}) 

class CreateInformDetailBank(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        codeInfD=request.GET.get('codeInfD')
        inform = InformBank.objects.get(id=request.GET.get('informId'))
        informDetailExist = InformBankDetall.objects.filter(codeInfD=codeInfD.upper(), inform_id=inform.id).exists()
        if informDetailExist == False:
            newInformDetail = InformBankDetall.objects.create(
            inform= inform, 
            codeInfD=codeInfD.upper(), 
            descriptionInfD=request.GET.get('descriptionInfD').upper(), 
            activity=request.GET.get('activity').upper()    
        )
            detalle= {'id':newInformDetail.id,'codeInfD':newInformDetail.codeInfD}
            return JsonResponse({'CREATE':"TRUE"})
        else:
            return JsonResponse({'CREATE':"FALSE"})
            

class UpdateInformBank(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def  get(self, request, *args, **kwargs):
        
        updateInformBank = InformBank.objects.get(id=request.GET.get('id'))
        nameI=request.GET.get('nameI').upper()
        if request.GET.get('equalName') == 'TRUE':
    
            updateInformBank.category = request.GET.get('category').upper()
            updateInformBank.digitI = request.GET.get('digitI')
            updateInformBank.save() 
            return JsonResponse({'CREATE':"TRUE"})
        else:
            informBankExist = InformBank.objects.filter(nameI=request.GET.get('nameI').upper(),bussines_id=request.GET.get('bussinesId')).exists()
            if informBankExist == False:
                updateInformBank.nameI = nameI
                updateInformBank.category = request.GET.get('category').upper()
                updateInformBank.digitI = request.GET.get('digitI')
                updateInformBank.save() 
                return JsonResponse({'CREATE':"TRUE"})
            else:
                return JsonResponse({'CREATE':"FALSE"})

class ChangeWindowsInformDetailBank(LoginRequiredMixin, View):
    print('hola soy')

    login_url = '/login/'
    redirect_field_name = '/login/'
    def get(self, request, *args, **kwargs):
        
        informDetailBank= InformBankDetall.objects.filter(inform_id=request.GET.get('informId')).values('codeInfD', 'descriptionInfD', 'activity')
    
        return JsonResponse({'IDB': list(informDetailBank)})


class ImportAccountsBD(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  post(self, request, *args, **kwargs):
   
        accountsArray = request.POST.get('accounts')
        accounts = json.loads(accountsArray)
        accountPeriod = request.POST.get('accountPeriod')
        for x in range(0,len(accounts)):
            accountExist = Account.objects.filter(code=accounts[x]['CD'],accountPeriod_id=accountPeriod).exists()
            if accountExist == False:
                if len(accounts[x]['CD']) != 1:
                    value = searchImport(request,accounts[x]['CD'],accountPeriod,1)
                    filaAccount=str(accounts[x]['CD'])
                    getAccount = Account.objects.get(code=filaAccount[:-request.session.get('numAC')],accountPeriod_id=accountPeriod)
                    if  accounts[x]['TC'] == "A":
                        newAccount = Account.objects.create(
                            accountPeriod_id = accountPeriod,code = accounts[x]['CD'], description = accounts[x]['DC'], state='ACTIVO' , corriente=accounts[x]['CO'], 
                            nature=accounts[x]['NT'], typeAccount='A', level =getAccount.level+1,accountFather= getAccount.id
                        )
                    else:
                        newAccount =Account.objects.create(
                            accountPeriod_id = accountPeriod,code = accounts[x]['CD'], description = accounts[x]['DC'], state='ACTIVO' , corriente=accounts[x]['CO'], 
                            nature=accounts[x]['NT'], typeAccount='M', level =getAccount.level+1,accountFather= getAccount.id
                        )

                else: 
                    if  accounts[x]['TC'] == "A":
                        newAccount = Account.objects.create(
                            accountPeriod_id = accountPeriod,code = accounts[x]['CD'], description = accounts[x]['DC'], state='ACTIVO' , corriente=accounts[x]['CO'], 
                            nature=accounts[x]['NT'], typeAccount='A', level =1
                        )
                    else:
                        newAccount = Account.objects.create(
                            accountPeriod_id = accountPeriod,code = accounts[x]['CD'], description = accounts[x]['DC'], state='ACTIVO' , corriente=accounts[x]['CO'], 
                            nature=accounts[x]['NT'], typeAccount='M', level =1
                        )                  
            else:
                return JsonResponse({"IMPORT": "FALSE"})
                break

        return JsonResponse({"IMPORT": "TRUE","ACCOUNTS": list(listAccount)})


def searchImport(request, account,accountPeriod,discount):
    
    accountExist = Account.objects.filter(code=account[:-discount],accountPeriod_id=accountPeriod).exists()
    
    if accountExist==False:
        searchImport(request,account,accountPeriod,discount+1)
    else:
        request.session['numAC'] = discount
        return discount

class SearchAccountButton(LoginRequiredMixin, View):
    print('hola soy')

    login_url = '/login/'
    redirect_field_name = '/login/'
    def get(self, request, *args, **kwargs):

        accountSearch = request.GET.get('account') #esta linea es para un diccionario
        accounts = Account.objects.filter(account__startswith=accountSearch,accountPeriod_id=accountPeriod) #lista de objectos medicamentos
        accounts = [ account_serializer(account) for account in accounts ] # lista de diccionario
        print(accounts)
        return HttpResponse(json.dumps(accounts), content_type='application/json')

    def account_serializer(account):
        return {'id': account.id, 'code': account.code, 'description': account.description}

class GetSearchAccountButton(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        print('hola función obtener cuenta')
        print(request.GET.get('idAC'))
        accounts = Account.objects.filter(accountPeriod_id=request.GET.get('idAC')).values('id','code', 'description')
        return JsonResponse({"ACCOUNT": list(accounts)})   

