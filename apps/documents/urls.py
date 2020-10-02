from django.conf.urls import url, include
from apps.documents.views import *

urlpatterns = [

    url(r'documents/listVoucher/(?P<pk>\d+)/$', ListVoucher.as_view() , name='listVoucher'),
    url(r'ajax/createVoucher', CreateVoucher.as_view(), name='createVoucher'),
    url(r'ajax/updateVoucher', UpdateVoucher.as_view(), name='updateVoucher'),
    url(r'documents/generateDocuments', generateDocuments , name='generateDocuments'),
    url(r'ajax/getVoucher', GetVoucher.as_view(), name='getVoucher'),
    
    url(r'documents/listThird/(?P<pk>\d+)/$', ListThird.as_view() , name='listThird'),
    url(r'ajax/createThird', CreateThird.as_view(), name='createThird'),
    url(r'ajax/updateThird', UpdateThird.as_view(), name='updateThird'),

    url(r'documents/listTypeContract/(?P<pk>\d+)/$', ListTypeContract.as_view() , name='listTypeContract'),
    url(r'ajax/createDetailTypeContract', CreateDetailTypeContract.as_view(), name='createDetailTypeContract'),
    url(r'ajax/createTypeContract', CreateTypeContract.as_view(), name='createTypeContract'),
    url(r'ajax/updateTypeContract', UpdateTypeContract.as_view(), name='updateTypeContract'),
    url(r'ajax/getDisponibility', GetDisponibility.as_view(), name='getDisponibility'),
    url(r'ajax/createDisponibility', CreateDisponibility.as_view(), name='createDisponibility'),
    url(r'ajax/getDetallsDisponibility', GetDetallsDisponibility.as_view(), name='getDetallsDisponibility'),
    url(r'ajax/getDataToRegister', GetDataToRegister.as_view(), name='getDataToRegister'),

]