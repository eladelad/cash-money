from django.conf.urls import patterns, url
from expenses import views

urlpatterns = patterns('',
                       url(r'^$', views.CategoryList.as_view(), name='list-create-category'),
                       url(r'^sub$', views.SubCategoryList.as_view(), name='list-create-sub-category'),
                       url(r'^sub/(?P<category>\d+)$', views.SubCategoryList.as_view(), name='list-create-sub-category-by-category'),
                       )