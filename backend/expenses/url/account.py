from django.conf.urls import patterns, url
from expenses import views

urlpatterns = patterns('',
                       url(r'^$', views.AccountList.as_view(), name='list-create-accounts'),
                       url(r'^$', views.PaymentTypeList.as_view(), name='list-create-paymenttype'),
                       )