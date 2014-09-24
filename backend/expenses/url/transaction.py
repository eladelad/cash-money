from django.conf.urls import patterns, url
from expenses import views

urlpatterns = patterns('',
                       url(r'^$', views.getOrCreateBoard.as_view(), name='list-create-transaction'),
                       )


# urlpatterns = patterns('',
#                        url(r'^(?P<boardname>[A-Za-z0-9\.\s\-_]+)$', views.getOrCreateBoard.as_view(), name='get-or-create-board'),
#                        url(r'^fav/add/(?P<boardid>\d+)$', views.favBoard.as_view(), name='add-board-favorite'),
#                        url(r'^fav/del/(?P<boardid>\d+)$', views.favBoard.as_view(), name='del-board-favorite'),
#                        url(r'^history/add/(?P<boardid>\d+)$', views.favBoard.as_view(), name='add-board-history'),
#                        url(r'^history/del/(?P<boardid>\d+)$', views.favBoard.as_view(), name='del-board-history'),
#                        url(r'^del/(?P<pk>\d+)$', views.BoardDel.as_view(), name='board-del'),
#                        url(r'^patch/(?P<pk>\d+)$', views.BoardPatch.as_view(), name='board-del'),
#                        url(r'^top$', views.HotBoards.as_view(), name='hot-board-list'),
#                        url(r'^search/(?P<search>[A-Za-z0-9\.\s\-_]+)$', views.BoardListSearch.as_view(), name='board-list-search'),
#                        )