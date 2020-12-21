from django.conf.urls import url, include
from apps.settingsSICAP.views import *

urlpatterns = [
    
    url(r'ajax/settingsOP/(?P<pkUser>\d+)/', GetOriginSettings.as_view(), name='settingsOP'),
    url(r'ajax/settingsOG/(?P<pkUser>\d+)/', CreateOriginSettings.as_view(), name='settingsOG'),
    url(r'ajax/settingsCreateOP/(?P<pkUser>\d+)/', CreateOperationSettings.as_view(), name='settingsCreateOP'),
    url(r'ajax/settingsInfDetall/(?P<pkUser>\d+)/', CreateInformDetall.as_view(), name='settingsInfDetall'),
    url(r'ajax/createInform/(?P<pkUser>\d+)/$', CreateInform.as_view(), name='createInform'), 
    url(r'settings/(?P<pk>\d+)/(?P<pkUser>\d+)/$', ListAccountPeriod.as_view() , name='settings'),
    url(r'settings/listInform/(?P<pk>\d+)/(?P<pkUser>\d+)/$', ListInform.as_view() , name='listInform'),
    url(r'settings/createTypeAgreement/(?P<pkUser>\d+)/', CreateTypeAgreement.as_view(), name='createTypeAgreement'), 
    url(r'settings/listTypeAgreement/(?P<pk>\d+)/(?P<pkUser>\d+)/$', ListTypeAgreement.as_view() , name='listTypeAgreement'),
    url(r'ajax/updateTypeAgreement/(?P<pkUser>\d+)/', UpdateTipeAgreement.as_view(), name='updateTypeAgreement'),
    url(r'settings/deleteAll/(?P<pkUser>\d+)/', DeleteAll.as_view() , name='deleteAll'),
    url(r'ajax/updateAccountPeriod/(?P<pkUser>\d+)/', UpdateAccountPeriod.as_view(), name='updateAccountPeriod'),
    url(r'ajax/updateInform/(?P<pkUser>\d+)/', UpdateInform.as_view(), name='updateInform'),
    url(r'settings/listOperations/(?P<pk>\d+)/(?P<pkUser>\d+)/', ListOperations.as_view() , name='listOperations'),
    url(r'ajax/updateOperation/(?P<pkUser>\d+)/', UpdateOperation.as_view(), name='updateOperation'),
    url(r'ajax/getOperationsContra/(?P<pkUser>\d+)/', GetOperationsContra.as_view(), name='getOperationsContra'),
    url(r'ajax/updateContraOperation/(?P<pkUser>\d+)/', UpdateContraOperation.as_view(), name='updateContraOperation'),
    url(r'ajax/getOriginOperation/(?P<pkUser>\d+)/', GetOriginOperation.as_view(), name='getOriginOperation'),
    url(r'ajax/changeWindowsOperation/(?P<pkUser>\d+)/', ChangeWindowsOperation.as_view(), name='changeWindowsOperation'),
    url(r'settings/listDiscount/(?P<pk>\d+)/(?P<pkUser>\d+)/$', ListDiscount.as_view() , name='listDiscount'),
    url(r'ajax/createDiscount/(?P<pkUser>\d+)/$', CreateDiscount.as_view(), name='createDiscount'),

    url(r'settings/listAccount/(?P<pk>\d+)/(?P<pkUser>\d+)/$', ListAccount.as_view() , name='listAccount'),
    url(r'ajax/createAccount/(?P<pkUser>\d+)/$', CreateAccount.as_view(), name='createAccount'),
    url(r'ajax/updateAccount/(?P<pkUser>\d+)/', UpdateAccount.as_view(), name='updateAccount'),

    url(r'settings/generateAccounting/(?P<pkUser>\d+)/', generateAccounting , name='generateAccounting'),
    url(r'ajax/getAccountSettings/(?P<pkUser>\d+)/', GetAccountSettings.as_view(), name='getAccountSettings'),
    url(r'ajax/createAccountingOpTip/(?P<pkUser>\d+)/$', CreateAccountingOpTip.as_view(), name='createAccountingOpTip'),
    url(r'ajax/getBudget/(?P<pkUser>\d+)/', GetBudget.as_view(), name='getBudget'),
    url(r'ajax/createAccountRubro/(?P<pkUser>\d+)/', CreateAccountRubro.as_view(), name='createAccountRubro'),
    url(r'ajax/getAccountsByRubro/(?P<pkUser>\d+)/', GetAccountsByRubro.as_view(), name='getAccountsByRubro'),
    url(r'ajax/searchAccount/(?P<pkUser>\d+)/', SearchAccount.as_view(), name='searchAccount'),
    
    url(r'settings/listInformBank/(?P<pk>\d+)/(?P<pkUser>\d+)/$', ListInformBank.as_view() , name='listInformBank'),
    url(r'ajax/createInformBank/(?P<pkUser>\d+)/$', CreateInformBank.as_view(), name='createInformBank'), 
    url(r'ajax/settingsInfDetailBank/(?P<pkUser>\d+)/', CreateInformDetailBank.as_view(), name='settingsInfDetailBank'),
    url(r'ajax/updateInformBank/(?P<pkUser>\d+)/', UpdateInformBank.as_view(), name='updateInformBank'),
    url(r'ajax/changeWindowsInformDetailBank/(?P<pkUser>\d+)/', ChangeWindowsInformDetailBank.as_view(), name='changeWindowsInformDetailBank'),
    url(r'ajax/importAccountsBD/(?P<pkUser>\d+)/', ImportAccountsBD.as_view(), name='importAccountsBD'),

    url(r'ajax/searchAccountButton/(?P<pkUser>\d+)/', SearchAccountButton.as_view(), name='searchAccountButton'),

    url(r'ajax/getSearchAccountButton/(?P<pkUser>\d+)/', GetSearchAccountButton.as_view(), name='getSearchAccountButton'),
    
]