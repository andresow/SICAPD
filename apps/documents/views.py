from django.shortcuts import render
from apps.documents.models import *
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from apps.documents.forms import *
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from datetime import date
from datetime import datetime
import simplejson as json
from tablib import Dataset 
from django.views.decorators.csrf import csrf_exempt
from apps.budgets.resources import RubroResources

# Create your views here.
#///////////////Document tatan
class ListVoucher(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = '/login/'
    model = Voucher
    queryset= model.objects.order_by('name')
    template_name = 'documents/listVoucher.html'

    def get_context_data(self):
        context = super(ListVoucher, self).get_context_data()
        context['voucherForm'] = VoucherForm
        context['voucherUpdateForm'] = ByVoucherUpdate
        return context  

    def get_queryset(self):
        queryset = super(ListVoucher, self).get_queryset()
        return Voucher.objects.filter(bussines_id=self.kwargs['pk'])
        
class CreateVoucher(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        today = datetime.now()
        bussinesId= request.GET.get('bussines')
        code = request.GET.get('code').upper()
        name = request.GET.get('name').upper()
        description = request.GET.get('description').upper()
        order = request.GET.get('order')
        number = request.GET.get('number')
        category = request.GET.get('category').upper()
 
        bussines = Bussines.objects.get(id=bussinesId)
        voucherExist = Voucher.objects.filter(name=name, bussines_id=bussinesId).exists()
        if voucherExist == False:
            newVoucher = Voucher.objects.create(
                bussines=bussines, code=code, name=name, description=description, order=order, number=int(number), category=category, dateCreation=today
            )
            return JsonResponse({'CREATE':"TRUE"})
        else:
            return JsonResponse({'CREATE':"FALSE"})

class UpdateVoucher(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def  get(self, request, *args, **kwargs): 
        
        updateVoucher = Voucher.objects.get(id=request.GET.get('id'))
        code = request.GET.get('code').upper()
        if request.GET.get('equalName') == 'TRUE':
            
            updateVoucher.code = request.GET.get('code').upper()
            updateVoucher.name = request.GET.get('name').upper()
            updateVoucher.description = request.GET.get('description').upper()
            updateVoucher.order = request.GET.get('order')
            updateVoucher.number = request.GET.get('number')
            updateVoucher.category = request.GET.get('category').upper()  
            updateVoucher.save()     
            return JsonResponse({'CREATE':"TRUE"})
        else:
            voucherExist = Voucher.objects.filter(code=code, bussines_id=request.GET.get('bussinesId')).exists()
            if voucherExist == False:
               
                updateVoucher.code = request.GET.get('code').upper()
                updateVoucher.name = request.GET.get('name').upper()
                updateVoucher.description = request.GET.get('description').upper()
                updateVoucher.order = request.GET.get('order')
                updateVoucher.number = request.GET.get('number')
                updateVoucher.category = request.GET.get('category').upper()  
                updateVoucher.save()  
                return JsonResponse({'CREATE':"TRUE"})
            else:
                return JsonResponse({'CREATE':"FALSE"}) 
        
def generateDocuments(request,pkUser):

    return render(request, 'documents/generateDocuments.html')

class GetVoucher(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
        if request.GET.get('option') == '1':
            bussinesId= request.GET.get('idBussines')
            voucher = Voucher.objects.filter(bussines_id=bussinesId).values('name')
            return JsonResponse({"VH": list(voucher)})
        elif request.GET.get('option') == '2':
            bussinesId= request.GET.get('idBussines')
            accountPeriod =  AccountPeriod.objects.get(bussines_id=bussinesId, name=request.GET.get('nameAC')[:-1])
            origin = Origin.objects.filter(accountPeriod_id=accountPeriod.id).exclude(nameOrigin='INGRESOS').values('nameOrigin')
            return JsonResponse({"OR": list(origin)})
        elif request.GET.get('option') == '3':
            bussinesId= request.GET.get('idBussines')
            accountPeriod =  AccountPeriod.objects.get(bussines_id=bussinesId, name=request.GET.get('nameAC')[:-1])
            origin = Origin.objects.get(accountPeriod_id=accountPeriod.id, nameOrigin=request.GET.get('origin'))
            return JsonResponse({"ID": origin.id})
        else:
            return JsonResponse({"else": "true"})

class ListThird(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = '/login/'
    model = Third
    queryset= model.objects.order_by('name')
    template_name = 'documents/listThird.html'

    def get_context_data(self):
        context = super(ListThird, self).get_context_data()
        context['thirdForm'] = ThirdForm
        context['byThirdUpdateForm'] = ByThirdUpdate
        return context  

    def get_queryset(self):
        queryset = super(ListThird, self).get_queryset()
        return Third.objects.filter(bussines_id=self.kwargs['pk'])
        
class CreateThird(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        bussinesId= request.GET.get('bussines')
        typeIdentification = request.GET.get('typeIdentification').upper()
        identification = request.GET.get('identification')
        name = request.GET.get('name').upper()
        surnames = request.GET.get('surnames').upper()
        reason = request.GET.get('reason').upper()
        phone = request.GET.get('phone')
        city = request.GET.get('city').upper()
 
        bussines = Bussines.objects.get(id=bussinesId)
        thirdExist = Third.objects.filter(name=name, bussines_id=bussinesId).exists()
        if thirdExist == False:
            newThird = Third.objects.create(
                bussines=bussines, typeIdentification=typeIdentification, identification=identification, name=name, surnames=surnames, reason=reason, phone=phone, city=city
            )
            return JsonResponse({'CREATE':"TRUE"})
        else:
            return JsonResponse({'CREATE':"FALSE"})

class UpdateThird(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def  get(self, request):
 
        updateThird = Third.objects.get(id=request.GET.get('id'))
        name = request.GET.get('name').upper()
        if request.GET.get('equalName') == 'TRUE':
            
            updateThird.typeIdentification = request.GET.get('typeIdentification').upper()
            updateThird.identification = request.GET.get('identification')
            updateThird.name = request.GET.get('name').upper()
            updateThird.surnames = request.GET.get('surnames').upper()
            updateThird.reason = request.GET.get('reason').upper()
            updateThird.phone = request.GET.get('phone')
            updateThird.city = request.GET.get('city').upper()  
            updateThird.save()     
            return JsonResponse({'CREATE':"TRUE"})
        else:
            thirdExist = Third.objects.filter(name=name, bussines_id=request.GET.get('bussinesId')).exists()
            if thirdExist == False:

                updateThird.typeIdentification = request.GET.get('typeIdentification').upper()
                updateThird.identification = request.GET.get('identification')
                updateThird.name = request.GET.get('name').upper()
                updateThird.surnames = request.GET.get('surnames').upper()
                updateThird.reason = request.GET.get('reason').upper()
                updateThird.phone = request.GET.get('phone')
                updateThird.city = request.GET.get('city').upper()  
                updateThird.save()  
                return JsonResponse({'CREATE':"TRUE"})
            else:
                return JsonResponse({'CREATE':"FALSE"}) 

class ListTypeContract(LoginRequiredMixin, ListView):

    login_url = '/login/'
    redirect_field_name = '/login/'
    model = TypeContract
    queryset= model.objects.order_by('name')
    template_name = 'documents/listTypeContract.html'

    def get_context_data(self):
        context = super(ListTypeContract, self).get_context_data()
        context['typeContractForm'] = TypeContractForm
        context['typeContractDetailForm'] = TypeContractDetailForm
        context['byTypeContractUpdateForm'] = ByTypeContractUpdate
        
        return context  

    def get_queryset(self):
        queryset = super(ListTypeContract, self).get_queryset()
        return TypeContract.objects.filter(bussines_id=self.kwargs['pk'])
        
class CreateTypeContract(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        bussinesId= request.GET.get('bussines')
        nameTC = request.GET.get('nameTC').upper()
        description = request.GET.get('description')
        categoryTC = request.GET.get('categoryTC').upper()
        digitsTC = request.GET.get('digitsTC').upper()
    
        bussines = Bussines.objects.get(id=bussinesId)
        typeContractExist = TypeContract.objects.filter(nameTC=nameTC, bussines_id=bussinesId).exists()
        if typeContractExist == False:
            newtypeContract = TypeContract.objects.create(
                bussines=bussines, nameTC=nameTC, description=description, categoryTC=categoryTC, digitsTC=digitsTC
            )
            return JsonResponse({'CREATE':"TRUE"})
        else:
            return JsonResponse({'CREATE':"FALSE"})

class CreateDetailTypeContract(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        codeTypeC=request.GET.get('codeTypeC')
        typeContract = TypeContract.objects.get(id=request.GET.get('typeContractId'))
        detailTypeContractExist = TypeContractDetail.objects.filter(codeTypeC=codeTypeC.upper(), typeContract_id=typeContract.id).exists()
        if detailTypeContractExist == False:
            newIdetailTypeContract = TypeContractDetail.objects.create(
            typeContract= typeContract, 
            codeTypeC=codeTypeC.upper(), 
            descriptionTypeC=request.GET.get('descriptionTypeC').upper(), 
            activity=request.GET.get('activity').upper()    
        )
            detalle= {'id':newIdetailTypeContract.id,'codeTypeC':newIdetailTypeContract.codeTypeC}
            return JsonResponse({'CREATE':"TRUE"})
        else:
            return JsonResponse({'CREATE':"FALSE"})

class UpdateTypeContract(LoginRequiredMixin, View):

    login_url = '/login/'
    redirect_field_name = '/login/'
    def  get(self, request, *args, **kwargs): 
        print('entre función actualizar')
        print(request.GET.get('bussinesId'))
        print(request.GET.get('typeContractId'))
        print(request.GET.get('nameTC'))
        print(request.GET.get('description'))
        print(request.GET.get('categoryTC'))
        print(request.GET.get('digitsTC'))
 
        updateTypeContract = TypeContract.objects.get(id=request.GET.get('id'))
        nameTC = request.GET.get('nameTC').upper()
        if request.GET.get('equalName') == 'TRUE':
            
            updateTypeContract.nameTC = request.GET.get('nameTC').upper()
            updateTypeContract.description = request.GET.get('description').upper()
            updateTypeContract.categoryTC = request.GET.get('categoryTC').upper()
            updateTypeContract.digitsTC = request.GET.get('digitsTC').upper()
            updateTypeContract.save()     
            return JsonResponse({'CREATE':"TRUE"})
        else:
            typeContractExist = TypeContract.objects.filter(nameTC=nameTC, bussines_id=request.GET.get('bussinesId')).exists()
            if typeContractExist == False:

                updateTypeContract.nameTC = request.GET.get('nameTC').upper()
                updateTypeContract.description = request.GET.get('description').upper()
                updateTypeContract.categoryTC = request.GET.get('categoryTC').upper()
                updateTypeContract.digitsTC = request.GET.get('digitsTC').upper()
                updateTypeContract.save()  
                return JsonResponse({'CREATE':"TRUE"})
            else:
                return JsonResponse({'CREATE':"FALSE"})

class GetDisponibility(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):
    
        today = datetime.now()
        disponibility = Movement.objects.filter(concept="DISPONIBILIDAD", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).exists()

        if disponibility == False:
            disponibilityFormat = str(today.year) + str(today.month)+str(today.day)+str(0)
            movements = Movement.objects.filter(origin_id=request.GET.get('origin'),concept="DISPONIBILIDAD").values('id','value','balance','disponibility','observation')
            return JsonResponse({"DI": disponibilityFormat,"MV": list(movements)})
        else:        
            lastDisponibility = Movement.objects.filter(concept="DISPONIBILIDAD", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).last()
            movements = Movement.objects.filter(origin_id=request.GET.get('origin'),concept="DISPONIBILIDAD").values('id','value','balance','disponibility','observation')
            return JsonResponse({"DI": lastDisponibility.disponibility+1,"MV": list(movements)})

class CreateDisponibility(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        today = datetime.now()
        disponibilitys = json.loads(request.GET.get('disponibilitys'))
        bussines=Bussines.objects.get(id=request.GET.get('bussines'))
        disponibility = Movement.objects.filter(concept="DISPONIBILIDAD", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).exists()

        if disponibility == False:
            disponibilityFormat = str(today.year) + str(today.month)+str(today.day)+str(0)
            disponibility = Movement.objects.create(
                bussines=bussines,concept="DISPONIBILIDAD",value=request.GET.get('value'),balance=request.GET.get('balance'),
                date=request.GET.get('date'),disponibility=request.GET.get('disponibilityCode'),origin=Origin.objects.get(id=request.GET.get('origin')),observation=request.GET.get('observation')
            )
            for x in range(0,len(disponibilitys)):
                rubroMov = RubroMovement.objects.create(bussines=bussines,value=disponibilitys[x]['value'],valueP=0,balance=disponibilitys[x]['balance'],date=today,nameRubro=disponibilitys[x]['id'],movement=disponibility) 

            return JsonResponse({"CREATE": "TRUE"})
        else:        
            lastDisponibility = Movement.objects.filter(concept="DISPONIBILIDAD", bussines_id=request.GET.get('bussines'), origin_id=request.GET.get('origin'),date=today).last()
            disponibility = Movement.objects.create(
                bussines=bussines,concept="DISPONIBILIDAD",value=request.GET.get('value'),balance=request.GET.get('balance'),
                date=request.GET.get('date'),disponibility=lastDisponibility.disponibility+1,origin=Origin.objects.get(id=request.GET.get('origin')),observation=request.GET.get('observation')
            )
            for x in range(0,len(disponibilitys)):
                rubroMov = RubroMovement.objects.create(bussines=bussines,value=disponibilitys[x]['value'],valueP=0,balance=disponibilitys[x]['balance'],date=today,nameRubro=disponibilitys[x]['id'],movement=disponibility) 

            return JsonResponse({"CREATE": "TRUE"})


class GetDetallsDisponibility(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        rubroMov = RubroMovement.objects.filter(movement_id=request.GET.get('disponibility')).values('nameRubro','value','balance')
        rubroList = []

        for x in range(0,len(list(rubroMov))):
            rubro = Rubro.objects.get(id=list(rubroMov)[x]['nameRubro'])
            rubroList.append({"rubro":rubro.rubro,"description":rubro.description,"realBudget":rubro.realBudget ,"value":list(rubroMov)[x]['value'],"balance":list(rubroMov)[x]['balance']})
        return JsonResponse({"RUBRO": list(rubroList)})

class GetDataToRegister(LoginRequiredMixin,View):

    login_url = '/login/'
    redirect_field_name = '/login/'

    def get(self, request, *args, **kwargs):

        third = Third.objects.filter(bussines_id=request.GET.get('bussines')).values('name','surnames')        
        typeContract = TypeContract.objects.filter(bussines_id=request.GET.get('bussines')).values('nameTC')
        movement = Movement.objects.filter(bussines_id=request.GET.get('bussines'),origin_id=request.GET.get('origin'), concept="DISPONIBILIDAD").values('disponibility')
        return JsonResponse({"TH": list(third), "TC":list(typeContract),"MV":list(movement)})
   