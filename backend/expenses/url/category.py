from django.conf.urls import patterns, url
from expenses import views

urlpatterns = patterns('',
                       url(r'^$', views.Category.as_view(), name='list-create-category'),
                       url(r'^sub$', views.SubCategory.as_view(), name='list-create-sub-category'),
                       url(r'^sub/(?P<category>\d+)$', views.SubCategory.as_view(), name='list-create-sub-category-by-category'),
                       )