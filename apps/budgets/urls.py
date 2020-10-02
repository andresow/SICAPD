from django.conf.urls import url, include
from apps.budgets.views import *

urlpatterns = [

    url(r'bussines/base', base , name='index'),
    url(r'budget/createBudget', mainBudget , name='menu'),
    url(r'bussines/createBussines', CreateBussines.as_view(), name='createBussines'), 
    url(r'bussines/listBussines', ListBussines.as_view(), name='listBussines'),
    url(r'ajax/createAC', CreateAccountPeriod.as_view(), name='createAccountPeriod'),
    url(r'ajax/createOriginAC', GetAccountPeriodOrigin.as_view(), name='getAccountPeriodOrigin'),
    url(r'ajax/createBudget', GetOriginBudget.as_view(), name='getOriginBudget'),
    url(r'bussines/createOperation', CreateOperation.as_view(), name='createOperation'),
    url(r'ajax/createAccountPeriodOp', GetAccountPeriodOperation.as_view(), name='getAccountPeriodOperation'),
    url(r'ajax/createAccounPeriodOriginOp', GetAccountPeriodOriginOperation.as_view(), name='getAccountPeriodOriginOperation'),   
    url(r'ajax/createOrigin', CreateOrigin.as_view(), name='createOrigin'),
    url(r'ajax/getOperationBudget', GetOperationBudget.as_view(), name='getOperationBudget'),
    url(r'ajax/searchRubroTw', SearchRubroTw.as_view(), name='searchRubroTw'),
    url(r'ajax/createRubro', CreateRubro.as_view(), name='createRubro'),
    url(r'ajax/getRubrosOrigin', GetRubrosOrigin.as_view(), name='getRubrosOrigin'),
    url(r'ajax/getOperationByOperate', GetOperationByOperate.as_view(), name='getOperationByOperate'),
    url(r'ajax/updateRubro', UpdateRubro.as_view(), name='updateRubro'),
    url(r'ajax/getRubrosContraOperation', GetRubrosContraOperation.as_view(), name='getRubrosContraOperation'),
    url(r'ajax/createOperations', CreateOperations.as_view(), name='createOperations'),
    url(r'settings/deleteRubro', DeleteRubro.as_view() , name='deleteRubro'),
    url(r'ajax/getDetailRubro', GetDetailRubro.as_view(), name='getDetailRubro'),
    url(r'budget/importRubro/(?P<idBussines>\d+)/(?P<idOrigin>\d+)/', ImportRubro, name='importRubro'),
    url(r'ajax/getDetallAgreement', GetDetallAgreement.as_view(), name='getDetallAgreement'),
    url(r'ajax/getRubroCreate', GetRubroCreate.as_view(), name='getRubroCreate'),
    url(r'ajax/importRubrosBD', ImportRubrosBD.as_view(), name='importRubrosBD'),
    url(r'ajax/getRubroOperationDetail', GetRubroOperationDetail.as_view(), name='getRubroOperationDetail'),
    url(r'ajax/getInformtUpdateRubro', GetInformtUpdateRubro.as_view(), name='getInformtUpdateRubro'),


]