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

]