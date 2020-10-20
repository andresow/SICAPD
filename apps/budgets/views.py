from django.shortcuts import render
from apps.budgets.models import *
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from apps.budgets.forms import *
from django.urls import reverse_lazy, reverse
from apps.settingsSICAP.forms import *
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from datetime import date
from datetime import datetime
import simplejson as json
from tablib import Dataset 
from django.views.decorators.csrf import csrf_exempt
from apps.budgets.resources import RubroResources
import sys
from django.db.models import Sum

# Create your views here.


class CreateBussines(CreateView):

    model = Bussines
    form_class = BussinesForm
    template_name = 'bussines/createBussines.html'
    success_url = reverse_lazy('listBussines')

class ListBussines(LoginRequiredMixin,ListView):

    model = Bussines
    queryset= model.objects.order_by('name')
    template_name = 'bussines/listBussines.html'

    def get_context_data(self):
        context = super(ListBussines, self).get_context_data()
        context['ACform'] = AccountPeriodForm
        context['Originform'] = OriginForm
        context['ByAccountOpforms'] = ByAccountOpForms
        context['Operationform'] = OperationForm
        return context

def base(request):
   
    return render(request, 'base/base.html')

###################### Vistas relacionadas con periodos contables ####################
class CreateAccountPeriod(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs): 

        bussinesId= request.GET.get('bussines')
        name = request.GET.get('name')
        state = request.GET.get('state')
        initialDate = request.GET.get('initialDate')
        finalDate = request.GET.get('finalDate')
        bussines = Bussines.objects.get(id=bussinesId)
        accountPeriodExist = AccountPeriod.objects.filter(name=name.upper(), bussines_id=bussinesId).exists()
        if accountPeriodExist == False:
            newAccountPeriod = AccountPeriod.objects.create(
                bussines=bussines, name=name.upper(), state=state.upper(), initialDate=initialDate, finalDate=finalDate
            )
            accountPeriod = {'id':newAccountPeriod.id,'name':newAccountPeriod.name}
            return JsonResponse({'CREATE':"TRUE"})
        else:
            return JsonResponse({'CREATE':"FALSE"})

class GetAccountPeriodOrigin(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        accountPeriod =  AccountPeriod.objects.all().filter(bussines_id=request.GET.get('bussinesIdO')).values('name')
        return JsonResponse({"AC": list(accountPeriod)})


class CreateOrigin(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        nameAccount = request.GET.get('accountPeriod')
        nameAccount = nameAccount[:-1]
        accountPeriod = AccountPeriod.objects.get(name=nameAccount.upper())

        originExist = Origin.objects.filter(nameOrigin=request.GET.get('nameOrigin').upper(), accountPeriod_id=accountPeriod).exists()
        if originExist == False:
            nameOrigin = request.GET.get('nameOrigin')
            codeOrigin = request.GET.get('codeOrigin')
            descriptionOrigin = request.GET.get('descriptionOrigin')

            newOrigin = Origin.objects.create(nameOrigin=nameOrigin.upper(),codeOrigin=codeOrigin.upper(),descriptionOrigin=descriptionOrigin.upper(),orderOrigin=request.GET.get('orderOrigin').upper(),finalDateOrigin=request.GET.get('finalDateOrigin'),accountPeriod=accountPeriod)
            origin = {'id':newOrigin.id,'name':newOrigin.nameOrigin}
            return JsonResponse({'CREATE':"TRUE"})
        else:
            return JsonResponse({'CREATE':"FALSE"})
        
def mainBudget(request,pkUser):

    informForm = ByInformForms()
    updateForm = ByRubroUpdate()
    context = {'informForm':informForm, 'updateForm': updateForm }
    return render(request, 'budget/budget.html', context)

class CreateOperation(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        origins = json.loads(request.GET.get('origin'))
        bussines=request.GET.get('bussines')
        for x in range(0,len(origins)):
            nameAccount = request.GET.get('accountPeriod')
            nameAccount = nameAccount
            accountPeriod = AccountPeriod.objects.get(name=nameAccount, bussines_id=bussines)
            
            getOrigin  = Origin.objects.get(nameOrigin=origins[x], accountPeriod_id=accountPeriod)
            objOrigin = Origin.objects.filter(nameOrigin=origins[x], accountPeriod_id=accountPeriod)
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

        
class GetAccountPeriodOperation(LoginRequiredMixin,View): # funcion para cargar el periodo contable

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
   
        idBussines = request.GET.get('bussinesIdOP') #id de la empresa porque el periodo contable esta relacionado con la empresa
        accountPeriod = AccountPeriod.objects.filter(bussines_id=idBussines).values('name')# se filtra por el id de la empresa el periodo contable
        return JsonResponse({"ACName": list(accountPeriod)})

class GetAccountPeriodOriginOperation(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        accountPeriod = AccountPeriod.objects.get(name=request.GET.get('accountPeriod'))
        origins = Origin.objects.filter(accountPeriod_id=accountPeriod.id).values('nameOrigin')# con el .values('nameOrigin') le paso a mi lista lo que necesito
        return JsonResponse({"OR": list(origins)})

class GetOriginBudget(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
       
        option =request.GET.get('option')
        if option =='1':
            nameAC = request.GET.get('nameAC')[:-1]
            accountPeriod = AccountPeriod.objects.get(name=nameAC, bussines_id=request.GET.get('idBussines'))
            origintest = Origin.objects.filter(accountPeriod_id=accountPeriod.id).values('nameOrigin')
            return JsonResponse({"OR": list(origintest)})
        elif  option=='2':
            inform  = Inform.objects.filter(bussines_id=request.GET.get('idBussines')).values('nameI')
            return JsonResponse({"IF": list(inform)})
        elif option=='3': 
            informDetallTest  = InformDetall.objects.filter(inform__nameI=request.GET.get('inform')).values('codeInfD')
            return JsonResponse({"IFD": list(informDetallTest)})
        elif option=='4': 
            typeAgreement  = TypeAgreement.objects.filter().values("nameTA")
            return JsonResponse({"TA": list(typeAgreement)})
        else:
            return JsonResponse({"INFORMATION": "FALSE"})

class GetOperationBudget(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        nameOrigin = request.GET.get('nameOrigin')
        accountPeriod = AccountPeriod.objects.get(name=request.GET.get('nameAC')[:-1])
        origin = Origin.objects.get(nameOrigin=nameOrigin, accountPeriod=accountPeriod.id)
        operations = Operation.objects.filter(origin=origin.id).values('nameOp')
        rubro = Rubro.objects.filter(origin_id=origin.id, bussines_id=request.GET.get('idBussines')).values('id','rubro','rubroFather','typeRubro','description','dateCreation','initialBudget','realBudget','budgetEject').order_by('rubro')
        movementIni = Agreement.objects.filter(origin_id=origin.id).values('id','descriptionAg','numberAg','typeAgreement')
        return JsonResponse({"ID":origin.id ,"OP": list(operations),"RUBRO": list(rubro),"AG":list(movementIni)})

class GetRubroCreate(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        origin = Origin.objects.get(id=request.GET.get('origin'))
        rubro = Rubro.objects.filter(origin_id=origin.id, bussines_id=request.GET.get('idBussines')).values('id','rubro','rubroFather','typeRubro','description','dateCreation','initialBudget','realBudget').order_by('rubro')
        return JsonResponse({"RUBRO": list(rubro)})

class CreateRubro(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        today = datetime.now()
        rubroExists = Rubro.objects.filter(rubro=request.GET.get('rubro'),bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin')).exists()
        if rubroExists == False:
            if len(request.GET.get('rubro')) == 1:
                if request.GET.get('typeRubro') == 'AUXILIAR':
                    rubro = Rubro.objects.create(
                        bussines = Bussines.objects.get(id=request.GET.get('bussines')), 
                        origin = Origin.objects.get(id=request.GET.get('origin')), 
                        rubro = request.GET.get('rubro'), nivel = request.GET.get('nivel'), description = request.GET.get('description'), dateCreation = today,budgetEject=request.GET.get('initialBudget'), initialBudget = request.GET.get('initialBudget'), typeRubro = "A", realBudget=request.GET.get('initialBudget'),  
                    )
                    inform = json.loads(request.GET.get('inform'))
                    informDetall = json.loads(request.GET.get('detallInform'))
                    for x in range(0,len(inform)):
                        objInform = Inform.objects.filter(nameI=inform[x], bussines_id=request.GET.get('bussines'))
                        objDetall = InformDetall.objects.filter(codeInfD=informDetall[x])

                        rubro.inform.add(*objInform)
                        rubro.informdetall.add(*objDetall)

                    movement = Movement.objects.create(
                        bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                        nameRubro = rubro.id, concept = 'CREACION', value = request.GET.get('initialBudget'), balance = request.GET.get('initialBudget'), date = today        
                    ) 
                    rubroMov = RubroMovement.objects.create(
                        bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                        value = request.GET.get('initialBudget'), valueP = request.GET.get('initialBudget'), balance = request.GET.get('initialBudget'), date = today, nameRubro = rubro.id, movement = movement     
                    ) 
                    rubroMov = RubroBalanceOperation.objects.create(
                        bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                        typeOperation = 'CREACION', value = request.GET.get('initialBudget'), balance = request.GET.get('initialBudget'), date = today, nameRubro = rubro.id,    
                    )
                else:
                    rubro = Rubro.objects.create(
                        bussines = Bussines.objects.get(id=request.GET.get('bussines')), 
                        origin = Origin.objects.get(id=request.GET.get('origin')), 
                        rubro = request.GET.get('rubro'), nivel = request.GET.get('nivel'), description = request.GET.get('description'), dateCreation = today, initialBudget = 0, typeRubro = "M",realBudget=0, budgetEject= 0,
                    )
                    movement = Movement.objects.create(
                        bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                        nameRubro = rubro.id, concept = 'CREACION', value = 0, balance = 0, date = today        
                    ) 
                    rubroMov = RubroMovement.objects.create(
                        bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                        value = 0, valueP = 0, balance = 0, date = today, nameRubro =rubro.id, movement = movement     
                    ) 
                    rubroMov = RubroBalanceOperation.objects.create(
                        bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                        typeOperation = 'CREACION', value = 0, balance = 0, date = today, nameRubro = rubro.id,    
                    )

            else:
                if request.GET.get('typeRubro') == 'AUXILIAR':
    
                    rubroFather = Rubro.objects.get(rubro=request.GET.get('rubroFather'),bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'))
                    rubro = Rubro.objects.create(
                        bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                        origin = Origin.objects.get(id=request.GET.get('origin')),
                        rubro = request.GET.get('rubro'),
                        rubroFather = rubroFather.id, 
                        nivel = request.GET.get('nivel'), description = request.GET.get('description'), dateCreation = today, initialBudget = request.GET.get('initialBudget'), typeRubro = "A", realBudget=request.GET.get('initialBudget'), budgetEject=request.GET.get('initialBudget'),
                    )
                    inform = json.loads(request.GET.get('inform'))
                    informDetall = json.loads(request.GET.get('detallInform'))
                    for x in range(0,len(inform)):
                        objInform = Inform.objects.filter(nameI=inform[x])
                        objDetall = InformDetall.objects.filter(codeInfD=informDetall[x])
                        rubro.inform.add(*objInform)
                        rubro.informdetall.add(*objDetall)

                    movement = Movement.objects.create(
                        bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                        nameRubro = rubro.id, concept = 'CREACION', value = request.GET.get('initialBudget'), balance = request.GET.get('initialBudget'), date = today
                    ) 
                    rubroMov = RubroMovement.objects.create(
                        bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                        value = request.GET.get('initialBudget'), valueP = request.GET.get('initialBudget'), balance = request.GET.get('initialBudget'), date = today, nameRubro = rubro.id, movement = movement    
                    ) 
                    rubroMov = RubroBalanceOperation.objects.create(
                        bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                        typeOperation = 'CREACION', value = request.GET.get('initialBudget'), balance = request.GET.get('initialBudget'), date = today, nameRubro = rubro.id,    
                    )              
                    rubroFatherValue(request, rubroFather.id, int(request.GET.get('initialBudget')))
                else:
                    rubroFather = Rubro.objects.get(rubro=request.GET.get('rubroFather'),bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'))
                    rubro = Rubro.objects.create(
                        bussines = Bussines.objects.get(id=request.GET.get('bussines')), 
                        origin = Origin.objects.get(id=request.GET.get('origin')), 
                        rubroFather = rubroFather.id, 
                        rubro = request.GET.get('rubro'), nivel = request.GET.get('nivel'), description = request.GET.get('description'), dateCreation = today, initialBudget = 0, typeRubro = "M", realBudget=0,budgetEject= 0
                    )
                    movement = Movement.objects.create(
                        bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                        nameRubro = rubro.id, concept = 'CREACION', value = 0, balance = 0, date = today        
                    ) 
                    rubroMov = RubroMovement.objects.create(
                        bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                        value = 0, valueP = 0, balance = 0, date = today, nameRubro = rubro.id, movement = movement     
                    ) 
                    rubroMov = RubroBalanceOperation.objects.create(
                        bussines = Bussines.objects.get(id=request.GET.get('bussines')),
                        typeOperation = 'CREACION', value = 0, balance = 0, date = today, nameRubro = rubro.id,    
                    )
            return JsonResponse({"CREATE": "TRUE"}) 
        else:
            return JsonResponse({"CREATE": "FALSE"})  
#////////////////// jva actulizar rubro////////////
class GetDetailRubro(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        
        rubros = Rubro.objects.filter(id=request.GET.get('id'), origin__nameOrigin=request.GET.get('origin'), bussines_id=request.GET.get('bussines')).values('id','origin_id','bussines_id','rubro','rubroFather','typeRubro','nivel','description','dateCreation','initialBudget','realBudget')
        return JsonResponse({"RUBRO": list(rubros)})

class GetInformtUpdateRubro(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        
        rubros = Rubro.objects.filter(id=request.GET.get('id')).values('inform__nameI','informdetall__codeInfD')
        return JsonResponse({"RUBRO": list(rubros)})

class UpdateRubro(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):      
        updateRubro = Rubro.objects.get(id=request.GET.get('id'))
        if updateRubro.typeRubro == 'A' and request.GET.get('typeRubro')=='M':
            rubroExists = Rubro.objects.filter(rubroFather=request.GET.get('id'),bussines_id=request.GET.get('idBussines'),origin_id=request.GET.get('origin')).exists()
            movementExists = Movement.objects.filter(nameRubro=request.GET.get('id')).exclude(concept='CREACION').exists()
            rubroMovement = RubroMovement.objects.filter(nameRubro=request.GET.get('id'), movement__concept='DISPONIBILIDAD').exists()
            if movementExists == False and rubroMovement == False:
                    
                updateRubro.typeRubro = 'M'
                updateRubro.description = request.GET.get('description')
                updateRubro.initialBudget = request.GET.get('initialBudget')
                updateRubro.save()
                inform = json.loads(request.GET.get('inform'))
                informDetall = json.loads(request.GET.get('detallInform'))
                rbList = list(Rubro.objects.filter(id=request.GET.get('id')).values('inform__nameI','informdetall__codeInfD'))
                if rbList[0]['inform__nameI'] != None:
                    for x in range(0,len(rbList)):
                        objInformG = Inform.objects.get(nameI=rbList[x]['inform__nameI'], bussines_id=request.GET.get('idBussines'))
                        objDetallG = InformDetall.objects.get(codeInfD=rbList[x]['informdetall__codeInfD'],inform_id=objInformG.id)

                        updateRubro.inform.remove(objInformG.id)
                        updateRubro.informdetall.remove(objDetallG.id)

                    for x in range(0,len(inform)):
                        objInform = Inform.objects.filter(nameI=inform[x], bussines_id=request.GET.get('idBussines'))
                        objDetall = InformDetall.objects.filter(codeInfD=informDetall[x])
                        updateRubro.inform.add(*objInform)
                        updateRubro.informdetall.add(*objDetall)
                        updateRubro.save()
                else:
                    updateRubro.description = request.GET.get('description')
                    for x in range(0,len(inform)):
                        objInform = Inform.objects.filter(nameI=inform[x], bussines_id=request.GET.get('idBussines'))
                        objDetall = InformDetall.objects.filter(codeInfD=informDetall[x])
                        updateRubro.inform.add(*objInform)
                        updateRubro.informdetall.add(*objDetall)
                        updateRubro.save()

                    originId = request.GET.get('origin')
                    origin = Origin.objects.get(id=originId)
                    rubro = Rubro.objects.filter(origin_id=origin.id, bussines_id=request.GET.get('idBussines')).values('id','rubro','rubroFather','typeRubro','description','dateCreation','initialBudget','realBudget').order_by('rubro')                       
                    
                    return JsonResponse({"RUBRO": list(rubro), "MOVIMIENTO": 'FALSE'})        
            else:
                return JsonResponse({"MOVIMIENTO": 'TRUE'})    

        elif updateRubro.typeRubro == 'A' and request.GET.get('typeRubro')=='A':
            movementExists = Movement.objects.filter(nameRubro=request.GET.get('id')).exclude(concept='CREACION').exists()
            rubroMovement = RubroMovement.objects.filter(nameRubro=request.GET.get('id'), movement__concept='DISPONIBILIDAD').exists()

            if movementExists == False and rubroMovement == False:
                updateRubro.description = request.GET.get('description')
                updateRubro.initialBudget = request.GET.get('initialBudget')
                inform = json.loads(request.GET.get('inform'))
                informDetall = json.loads(request.GET.get('detallInform'))
                rbList = list(Rubro.objects.filter(id=request.GET.get('id')).values('inform__nameI','informdetall__codeInfD'))
                if rbList[0]['inform__nameI'] != None:
                    for x in range(0,len(rbList)):
                        objInformG = Inform.objects.get(nameI=rbList[x]['inform__nameI'], bussines_id=request.GET.get('idBussines'))
                        objDetallG = InformDetall.objects.get(codeInfD=rbList[x]['informdetall__codeInfD'],inform_id=objInformG.id)

                        updateRubro.inform.remove(objInformG.id)
                        updateRubro.informdetall.remove(objDetallG.id)

                    for x in range(0,len(inform)):
                        objInform = Inform.objects.filter(nameI=inform[x], bussines_id=request.GET.get('idBussines'))
                        objDetall = InformDetall.objects.filter(codeInfD=informDetall[x])
                        updateRubro.inform.add(*objInform)
                        updateRubro.informdetall.add(*objDetall)
                        updateRubro.save()
                else:
                    updateRubro.description = request.GET.get('description')
                    for x in range(0,len(inform)):
                        objInform = Inform.objects.filter(nameI=inform[x], bussines_id=request.GET.get('idBussines'))
                        objDetall = InformDetall.objects.filter(codeInfD=informDetall[x])
                        updateRubro.inform.add(*objInform)
                        updateRubro.informdetall.add(*objDetall)
                        updateRubro.save()

                    originId = request.GET.get('origin')
                    origin = Origin.objects.get(id=originId)
                    rubro = Rubro.objects.filter(origin_id=origin.id, bussines_id=request.GET.get('idBussines')).values('id','rubro','rubroFather','typeRubro','description','dateCreation','initialBudget','realBudget').order_by('rubro')                      
                    
                    return JsonResponse({"RUBRO": list(rubro), "MOVIMIENTO": 'FALSE'})        
            else:
                return JsonResponse({"MOVIMIENTO": 'TRUE'})

        elif updateRubro.typeRubro == 'M' and request.GET.get('typeRubro')=='A':
            rubroExists = Rubro.objects.filter(rubroFather=request.GET.get('id'),bussines_id=request.GET.get('idBussines'),origin_id=request.GET.get('origin')).exists()
            if updateRubro.description == request.GET.get('description'):
                    return JsonResponse({"DESCRIPTION": 'TRUE'})
            if rubroExists == False:           
                updateRubro.description = request.GET.get('description')
                updateRubro.typeRubro = 'A'
                updateRubro.save()                             
                originId = request.GET.get('origin')
                origin = Origin.objects.get(id=originId)
                rubro = Rubro.objects.filter(origin_id=origin.id, bussines_id=request.GET.get('idBussines')).values('id','rubro','rubroFather','typeRubro','description','dateCreation','initialBudget','realBudget').order_by('rubro')                               
                return JsonResponse({"RUBRO": list(rubro), "SOY_FATHER": 'FALSE'})
            else:
                return JsonResponse({"SOY_FATHER": 'TRUE'})  
        else:
            updateRubro.description = request.GET.get('description')
            updateRubro.typeRubro = 'A'
            updateRubro.save()  
            originId = request.GET.get('origin')
            origin = Origin.objects.get(id=originId)
            rubro = Rubro.objects.filter(origin_id=origin.id, bussines_id=request.GET.get('idBussines')).values('id','rubro','rubroFather','typeRubro','description','dateCreation','initialBudget','realBudget').order_by('rubro')                               
            return JsonResponse({"RUBRO": list(rubro), "SOY_FATHER": 'FALSE'})
                   
        

class DeleteRubro(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def get(self, request, *args, **kwargs):
        deleteRubro = Rubro.objects.get(id=request.GET.get('id'))
        option = request.GET.get('option')
        if deleteRubro.typeRubro == 'M':
            rubroExists = Rubro.objects.filter(rubroFather=request.GET.get('id'),bussines_id=request.GET.get('idBussines'),origin_id=request.GET.get('origin')).exists()
            if rubroExists == False:
                if option=='1':
                    deleteRubro = Rubro.objects.get(id=request.GET.get('id'))
                    deleteRubro.delete()
                    
                    originId = request.GET.get('origin')
                    origin = Origin.objects.get(id=originId)
                    rubro = Rubro.objects.filter(origin_id=origin.id, bussines_id=request.GET.get('idBussines')).values('id','rubro','rubroFather','typeRubro','description','dateCreation','initialBudget').order_by('rubro')
                    
                    return JsonResponse({'ELIMINADO': 'TRUE', "RUBRO": list(rubro)})
                else:
                    return JsonResponse({'ELIMINADO': 'FALSE'})
            else:
                return JsonResponse({"SOY_FATHER": 'TRUE'})
        else:
            movementExists = Movement.objects.filter(nameRubro=request.GET.get('id')).exclude(concept='CREACION').exists()
            rubroMovement = RubroMovement.objects.filter(nameRubro=request.GET.get('id'), movement__concept='DISPONIBILIDAD').exists()
            if movementExists == False and rubroMovement == False:
                deleteRubro = Rubro.objects.get(id=request.GET.get('id'))
                deleteRubro.delete()
                   
                originId = request.GET.get('origin')
                origin = Origin.objects.get(id=originId)
                rubro = Rubro.objects.filter(origin_id=origin.id, bussines_id=request.GET.get('idBussines')).values('id','rubro','rubroFather','typeRubro','description','dateCreation','initialBudget','realBudget').order_by('rubro')
                        
                return JsonResponse({'ELIMINADO': 'TRUE', "RUBRO": list(rubro)})        
            else:
                return JsonResponse({'MOVEMENTS': 'TRUE'}) 

class GetRubrosOrigin(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        rubros = Rubro.objects.filter(origin_id=request.GET.get('origin'), bussines_id=request.GET.get('bussines')).values('id','rubro','typeRubro','description','initialBudget','realBudget','budgetEject').order_by('rubro')
        return JsonResponse({"RUBRO": list(rubros)}) 

class GetOperationByOperate(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        origin = Origin.objects.get(id=request.GET.get('origin'))
        operation = Operation.objects.get(nameOp=request.GET.get('operation'), origin=origin)
        if operation.contraOperar == None:
            return JsonResponse({"OP": operation.operation,"CO": "No tiene agregado contraoperaciones"}) 
        else:
            contraOperation = Operation.objects.get(id=operation.contraOperar)
            return JsonResponse({"OP": operation.operation,"CO": contraOperation.nameOp}) 

class GetRubrosContraOperation(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        operation = Operation.objects.get(nameOp=request.GET.get('operation'), origin=Origin.objects.get(id=request.GET.get('origin')))
        idContraOperation = operation.contraOperar
        contraoperation = Operation.objects.get(id=idContraOperation)
        rubros = Rubro.objects.filter(origin_id=operation.contraOrigin, bussines_id=request.GET.get('bussines')).values('id','rubro','typeRubro','description','initialBudget','realBudget').order_by('rubro')
        return JsonResponse({"RUBRO": list(rubros), "CONTRAOPERACION": str(contraoperation.operation),"NAME": contraoperation.nameOp}) 

class CreateOperations(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def post(self, request, *args, **kwargs):
        agreement = Agreement.objects.create(
           origin_id = request.POST.get('origin'),
           numberAg = request.POST.get('number'),
           descriptionAg = request.POST.get('concept'),
           dateAg = request.POST.get('date'),
           typeAgreement = TypeAgreement.objects.get(nameTA=request.POST.get('typeAgreement'), bussines_id=request.POST.get('bussines'))
        )

        operation = json.loads(request.POST.get('operation'))
        contraoperation = json.loads(request.POST.get('contraoperation'))
        bussines = Bussines.objects.get(id=request.POST.get('bussines'))
        agreement =  Agreement.objects.last()
        today = datetime.now()
        for x in range(0,len(operation)):
            bussines = Bussines.objects.get(id=request.POST.get('bussines'))
            rubro = Rubro.objects.get(id=operation[x]['id'])
            movement = Movement.objects.create(bussines=bussines,nameRubro=operation[x]['id'],concept=operation[x]['concept'], value=operation[x]['value'],balance=operation[x]['balance'],date=today,agreement=agreement,budgetEject=operation[x]['byEject'])
            rubroMov = RubroMovement.objects.create(bussines = bussines,value=operation[x]['value'],valueP=rubro.realBudget,balance=operation[x]['balance'],date=today,nameRubro=operation[x]['id'],movement=movement) 
            rubroBalanceMov = RubroBalanceOperation.objects.create(bussines=bussines,typeOperation=operation[x]['concept'],value=operation[x]['value'],balance=operation[x]['balance'],date=today,nameRubro=operation[x]['id']) 
            rubro.realBudget = operation[x]['balance']
            rubro.budgetEject = operation[x]['byEject']
            rubro.save()

        for x in range(0,len(contraoperation)):
            contraRubro = Rubro.objects.get(id=contraoperation[x]['id'])
            contramovement = Movement.objects.create(bussines=bussines,nameRubro=contraoperation[x]['id'],concept=contraoperation[x]['concept'], value=contraoperation[x]['value'],balance=contraoperation[x]['balance'],date=today,agreement=agreement,budgetEject=contraoperation[x]['byEject'])
            contraRubroMov = RubroMovement.objects.create(bussines = bussines,value=contraoperation[x]['value'],valueP=contraRubro.realBudget,balance=contraoperation[x]['balance'],date=today,nameRubro=contraoperation[x]['id'],movement=contramovement) 
            contraRubroBalanceMov = RubroBalanceOperation.objects.create(bussines=bussines,typeOperation=contraoperation[x]['concept'],value=contraoperation[x]['value'],balance=contraoperation[x]['balance'],date=today,nameRubro=contraoperation[x]['id']) 
            contraRubro.realBudget = contraoperation[x]['balance']
            contraRubro.budgetEject = contraoperation[x]['byEject']
            contraRubro.save()

        return JsonResponse({"OP":"TRUE"}) 

def ImportRubro(request,idBussines, idOrigin):

    if request.method == 'POST':
        rubroResource = RubroResources()  
        dataset = Dataset() 
        newRubros = request.FILES['myfile']  
        importedData = dataset.load(newRubros.read())  
        today = datetime.now()
        for fila in importedData:
            rubroExists = Rubro.objects.filter(rubro=fila[1],bussines_id=idBussines,origin_id=idOrigin).exists()
            if rubroExists == False:
                if len(fila[1]) != 1:
                    value = searchImport(request,fila[1],idOrigin,idBussines,1)
                    filaRubro=str(fila[1])
                    getRubro = Rubro.objects.get(rubro=filaRubro[:-request.session.get('num')],bussines_id=idBussines,origin_id=idOrigin)
                    if  fila[0] == "A":
                        Rubro.objects.create(
                            bussines_id = idBussines,origin_id = idOrigin, rubroFather= getRubro.id, 
                            rubro = fila[1], nivel =getRubro.nivel+1, description = fila[2], dateCreation = today, initialBudget =fila[3] , typeRubro = "A", realBudget=fila[3], imported="TRUE", 
                        )
                    else:
                        Rubro.objects.create(
                            bussines_id = idBussines, 
                            origin_id = idOrigin, rubroFather= getRubro.id,
                            rubro = fila[1], nivel =  getRubro.nivel+1, description = fila[2], dateCreation = today, initialBudget =fila[3] , typeRubro = "M", realBudget=fila[3], imported="TRUE",
                        )
                else: 
                    if  fila[0] == "A":
                        Rubro.objects.create(
                                bussines_id = idBussines,origin_id = idOrigin, 
                                rubro = fila[1], nivel = 1, description = fila[2], dateCreation = today, initialBudget =fila[3] , typeRubro = "A", realBudget=fila[3], imported="TRUE", 
                        )
                    else:
                        Rubro.objects.create(
                                bussines_id = idBussines, origin_id = idOrigin, 
                                rubro = fila[1], nivel = 1, description = fila[2], dateCreation = today, initialBudget =fila[3] , typeRubro = "M", realBudget=fila[3], imported="TRUE",
                        )                    
            else:
                break
        return render(request, 'budget/chargeRubro.html')
    else:     
        return render(request, 'budget/chargeRubro.html')

class SearchRubroTw(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        
        rubroLen = request.GET.get('rubro')
        if len(rubroLen) == 1:
            return JsonResponse({"RUBROFATHER": "PRIMER RUBRO"})
        else:  
            rubroExists = Rubro.objects.get(rubro=request.GET.get('rubro'),bussines_id=request.GET.get('idBussines'),origin_id=request.GET.get('origin'))
            last = Rubro.objects.all().last()
            return JsonResponse({"RUBROFATHER": "TRUE", "LEVEL":rubroExists.nivel+1, "LAST":last.rubro, "TYPERUBRO": rubroExists.typeRubro})


def rubroFatherValue(request, rubroFather, value):

    rubroFather = Rubro.objects.get(id=rubroFather)   
    currentRealBudget = rubroFather.realBudget
    newRealBudget = currentRealBudget + value
    rubroFather.realBudget = newRealBudget
    rubroFather.budgetEject = newRealBudget
    rubroFather.save()
    if rubroFather.rubroFather == None:
        return True
    else:        
        return rubroFatherValue(request, rubroFather.rubroFather, newRealBudget)


def searchImport(request, rubro,origin,bussines,discount):
    
    rubroExist = Rubro.objects.filter(rubro=rubro[:-discount],bussines_id=bussines,origin_id=origin).exists()
    
    if rubroExist==False:
        searchImport(request,rubro,origin,bussines,discount+1)
    else:
        request.session['num'] = discount
        return discount



class GetDetallAgreement(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        movements =  Movement.objects.filter(agreement_id=request.GET.get('agreement')).values('concept','value','balance','date')
        return JsonResponse({"MV": list(movements)})

class GetRubroOperationDetail(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):
        movements = RubroBalanceOperation.objects.filter(nameRubro=request.GET.get('id')).values('typeOperation','value','balance','date')
        return JsonResponse({"MVRUBRO": list(movements)})



class ImportRubrosBD(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  post(self, request, *args, **kwargs):
   
        bussines = request.POST.get('idBussines')
        rubrost = request.POST.get('rubros')
        rubros = json.loads(rubrost)
        origin = request.POST.get('origin')
        today = datetime.now()
        for x in range(0,len(rubros)):
            rubroExists = Rubro.objects.filter(rubro=rubros[x]['RB'],bussines_id=bussines,origin_id=origin).exists()
            if rubroExists == False:
                if len(rubros[x]['RB']) != 1:
                    value = searchImport(request,rubros[x]['RB'],origin,bussines,1)
                    filaRubro=str(rubros[x]['RB'])
                    getRubro = Rubro.objects.get(rubro=filaRubro[:-request.session.get('num')],bussines_id=bussines,origin_id=origin)
                    if  rubros[x]['TC'] == "A":
                        newRubro = Rubro.objects.create(
                            bussines_id = bussines,origin_id = origin, rubroFather= getRubro.id, 
                            rubro = rubros[x]['RB'], nivel =getRubro.nivel+1, description = rubros[x]['DC'], dateCreation = today, initialBudget =rubros[x]['PI'] , typeRubro = "A", realBudget=rubros[x]['PI'],budgetEject=rubros[x]['PI'], imported="TRUE"
                        )
                        movement = Movement.objects.create(bussines = bussines, nameRubro = newRubro.id, concept = 'CREACION', value = rubros[x]['PI'], balance = rubros[x]['PI'], date = today) 
                    else:
                        newRubro =Rubro.objects.create(
                            bussines_id = bussines, 
                            origin_id = origin, rubroFather= getRubro.id,
                            rubro = rubros[x]['RB'], nivel =  getRubro.nivel+1, description = rubros[x]['DC'], dateCreation = today, initialBudget =rubros[x]['PI'] , typeRubro = "M", realBudget=rubros[x]['PI'],budgetEject=rubros[x]['PI'], imported="TRUE"
                        )
                        movement = Movement.objects.create(bussines = bussines, nameRubro = newRubro.id, concept = 'CREACION', value = rubros[x]['PI'], balance = rubros[x]['PI'], date = today) 

                else: 
                    if  rubros[x]['TC'] == "A":
                        newRubro = Rubro.objects.create(
                                bussines_id = bussines,origin_id = origin, 
                                rubro = rubros[x]['RB'], nivel = 1, description = rubros[x]['DC'], dateCreation = today, initialBudget =rubros[x]['PI'] , typeRubro = "A", realBudget=rubros[x]['PI'],budgetEject=rubros[x]['PI'], imported="TRUE"
                        )
                        movement = Movement.objects.create(bussines = bussines, nameRubro = newRubro.id, concept = 'CREACION', value = rubros[x]['PI'], balance = rubros[x]['PI'], date = today)                 
                    else:
                        newRubro = Rubro.objects.create(
                                bussines_id = bussines, origin_id = origin, 
                                rubro = rubros[x]['RB'], nivel = 1, description = rubros[x]['DC'], dateCreation = today, initialBudget =rubros[x]['PI'] , typeRubro = "M", realBudget=rubros[x]['PI'], budgetEject=rubros[x]['PI'],imported="TRUE"
                        ) 
                        movement = Movement.objects.create(bussines = bussines, nameRubro = newRubro.id, concept = 'CREACION', value = rubros[x]['PI'], balance = rubros[x]['PI'], date = today) 
                   
            else:
                return JsonResponse({"IMPORT": "FALSE"})
                break

        rubros = Rubro.objects.filter(bussines_id=bussines,origin_id=origin).values('id','rubro','description','initialBudget','typeRubro').order_by('rubro')
        return JsonResponse({"IMPORT": "TRUE","RUBRO": list(rubros)})

class UpdateAgreementRubro(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def  get(self, request, *args, **kwargs):

        updateAgreement = Agreement.objects.get(id=request.GET.get('id'))
        listAgreement = Agreement.objects.filter(origin_id=request.GET.get('origin')).values('id', 'typeAgreement', 'numberAg', 'descriptionAg')
        
        updateAgreement.numberAg = request.GET.get('numberAg')
        updateAgreement.dateAg = request.GET.get('dateAg')
        updateAgreement.descriptionAg = request.GET.get('descriptionAg').upper()
        updateAgreement.save()

        return JsonResponse({'CREATE':"TRUE", 'AG':list(listAgreement)})

class DeleteRubrosImported(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  post(self, request, *args, **kwargs):

        rubrost = request.POST.get('rubros')
        rubros = json.loads(rubrost)
        for x in range(0,len(rubros)):
            rubro = Rubro.objects.get(bussines_id=request.POST.get('idBussines'),origin_id = request.POST.get('origin'),rubro=rubros[x]['RB'],imported="TRUE")
            if rubro != None:
                rubro.delete()
            else:
                print("gg")

        return JsonResponse({"DELETE": "TRUE"})

class GetMovementsByOrigin(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        movement = Movement.objects.filter(origin_id=request.GET.get('origin')).exclude(concept='CREACION').exists()
        if movement == True:
            return JsonResponse({"MOVEMENTS": "TRUE"})
        else:
            return JsonResponse({"MOVEMENTS": "FALSO"})

class GetDisponibilityByRubros(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def  get(self, request, *args, **kwargs):

        rubroMovement = RubroMovement.objects.filter(nameRubro=request.GET.get('id'),movement__concept='DISPONIBILIDAD').exists()
        if rubroMovement == True:
            rubroMovement = RubroMovement.objects.filter(nameRubro=request.GET.get('id'),movement__concept='DISPONIBILIDAD').aggregate(total_value=Sum('value'))
            print(rubroMovement)
            return JsonResponse({"DP": rubroMovement['total_value']})
        else:
            return JsonResponse({"DP": 0})
