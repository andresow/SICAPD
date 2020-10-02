from django.conf.urls import url, include
from apps.settingsSICAP.views import *

urlpatterns = [
    
    url(r'ajax/settingsOP', GetOriginSettings.as_view(), name='settingsOP'),
    url(r'ajax/settingsOG', CreateOriginSettings.as_view(), name='settingsOG'),
    url(r'ajax/settingsCreateOP', CreateOperationSettings.as_view(), name='settingsCreateOP'),
    url(r'ajax/settingsInfDetall', CreateInformDetall.as_view(), name='settingsInfDetall'),
    url(r'ajax/createInform/$', CreateInform.as_view(), name='createInform'), 
    url(r'settings/(?P<pk>\d+)/$', ListAccountPeriod.as_view() , name='settings'),
    url(r'settings/listInform/(?P<pk>\d+)/$', ListInform.as_view() , name='listInform'),
    url(r'settings/createTypeAgreement', CreateTypeAgreement.as_view(), name='createTypeAgreement'), 
    url(r'settings/listTypeAgreement/(?P<pk>\d+)/$', ListTypeAgreement.as_view() , name='listTypeAgreement'),
    url(r'ajax/updateTypeAgreement', UpdateTipeAgreement.as_view(), name='updateTypeAgreement'),
    url(r'settings/deleteAll', DeleteAll.as_view() , name='deleteAll'),
    url(r'ajax/updateAccountPeriod', UpdateAccountPeriod.as_view(), name='updateAccountPeriod'),
    url(r'ajax/updateInform', UpdateInform.as_view(), name='updateInform'),
    url(r'settings/listOperations/(?P<pk>\d+)/$', ListOperations.as_view() , name='listOperations'),
    url(r'ajax/updateOperation', UpdateOperation.as_view(), name='updateOperation'),
    url(r'ajax/getOperationsContra', GetOperationsContra.as_view(), name='getOperationsContra'),
    url(r'ajax/updateContraOperation', UpdateContraOperation.as_view(), name='updateContraOperation'),
    url(r'ajax/getOriginOperation', GetOriginOperation.as_view(), name='getOriginOperation'),
    url(r'ajax/changeWindowsOperation', ChangeWindowsOperation.as_view(), name='changeWindowsOperation'),
    
]