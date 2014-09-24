from django.conf.urls import patterns, url
from expenses import views

urlpatterns = patterns('',
                       url(r'^$', views.Account.as_view(), name='list-create-accounts'),
                       url(r'^$', views.PaymentType.as_view(), name='list-create-paymenttype'),
                       )