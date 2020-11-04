from django.conf.urls import url, include
from apps.documents.views import *

urlpatterns = [

    url(r'documents/listVoucher/(?P<pk>\d+)/(?P<pkUser>\d+)/$', ListVoucher.as_view() , name='listVoucher'),
    url(r'ajax/createVoucher/(?P<pkUser>\d+)/', CreateVoucher.as_view(), name='createVoucher'),
    url(r'ajax/updateVoucher/(?P<pkUser>\d+)/', UpdateVoucher.as_view(), name='updateVoucher'),
    url(r'documents/generateDocuments/(?P<pkUser>\d+)/', generateDocuments , name='generateDocuments'),
    url(r'ajax/getVoucher/(?P<pkUser>\d+)/', GetVoucher.as_view(), name='getVoucher'),   
    url(r'documents/listThird/(?P<pk>\d+)/(?P<pkUser>\d+)/$', ListThird.as_view() , name='listThird'),
    url(r'ajax/createThird/(?P<pkUser>\d+)/', CreateThird.as_view(), name='createThird'),
    url(r'ajax/updateThird/(?P<pkUser>\d+)/', UpdateThird.as_view(), name='updateThird'),
    url(r'documents/listTypeContract/(?P<pk>\d+)/(?P<pkUser>\d+)/$', ListTypeContract.as_view() , name='listTypeContract'),
    url(r'ajax/createDetailTypeContract/(?P<pkUser>\d+)/', CreateDetailTypeContract.as_view(), name='createDetailTypeContract'),
    url(r'ajax/createTypeContract/(?P<pkUser>\d+)/', CreateTypeContract.as_view(), name='createTypeContract'),
    url(r'ajax/updateTypeContract/(?P<pkUser>\d+)/', UpdateTypeContract.as_view(), name='updateTypeContract'),
    url(r'ajax/getDisponibility/(?P<pkUser>\d+)/', GetDisponibility.as_view(), name='getDisponibility'),
    url(r'ajax/createDisponibility/(?P<pkUser>\d+)/', CreateDisponibility.as_view(), name='createDisponibility'),
    url(r'ajax/getDetallsDisponibility/(?P<pkUser>\d+)/', GetDetallsDisponibility.as_view(), name='getDetallsDisponibility'),
    url(r'ajax/getDataToRegister/(?P<pkUser>\d+)/', GetDataToRegister.as_view(), name='getDataToRegister'),
    url(r'ajax/getDataRubroDisponibility/(?P<pkUser>\d+)/', GetDataRubroDisponibility.as_view(), name='getDataRubroDisponibility'),
    url(r'ajax/getOperationsByOrigin/(?P<pkUser>\d+)/', GetOperationsByOrigin.as_view(), name='getOperationsByOrigin'),
    url(r'ajax/getDisponibilityRegister/(?P<pkUser>\d+)/', GetDisponibilityRegister.as_view(), name='getDisponibilityRegister'),
    url(r'ajax/getThirds/(?P<pkUser>\d+)/', GetThirds.as_view(), name='getThirds'),
    url(r'ajax/fillDisponibility/(?P<pkUser>\d+)/', FillDisponibility.as_view(), name='fillDisponibility'),
    url(r'ajax/getRegisterSerial/(?P<pkUser>\d+)/', GetRegisterSerial.as_view(), name='getRegisterSerial'),
    url(r'ajax/createRegister/(?P<pkUser>\d+)/', CreateRegister.as_view(), name='createRegister'),
    url(r'ajax/getDataToObligation/(?P<pkUser>\d+)/', GetDataToObligation.as_view(), name='getDataToObligation'),
    url(r'ajax/getObligationSerial/(?P<pkUser>\d+)/', GetObligationSerial.as_view(), name='getObligationSerial'),
    url(r'ajax/fillRegister/(?P<pkUser>\d+)/', FillRegister.as_view(), name='fillRegister'),
    url(r'ajax/getRegistersOB/(?P<pkUser>\d+)/', GetRegistersOB.as_view(), name='getRegistersOB'),
    url(r'ajax/createObligation/(?P<pkUser>\d+)/', CreateObligation.as_view(), name='createObligation'),
    url(r'ajax/getObligationsVC/(?P<pkUser>\d+)/', GetObligationsVC.as_view(), name='getObligationsVC'),
    url(r'ajax/getDataToVoucherPayment/(?P<pkUser>\d+)/', GetDataToVoucherPayment.as_view(), name='getDataToVoucherPayment'),
    url(r'ajax/getSerialVoucherPayment/(?P<pkUser>\d+)/', GetSerialVoucherPayment.as_view(), name='getSerialVoucherPayment'),

]