from expenses.models import *
from expenses.serializers import *
from expenses.permissions import *

from django.core import serializers
from django.utils import timezone

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings

from expenses.views.core import *

class Category(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Category.objects.filter(Q(user=None) | Q(user=self.request.user)).distinct()


class SubCategory(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if 'category' in self.kwargs:
            return SubCategory.objects.filter(Q(category=self.kwargs['category']), Q(user=None) | Q(user=self.request.user)).distinct()
        else:
            return SubCategory.objects.filter(Q(user=None) | Q(user=self.request.user)).distinct()


# class addShareToBoard(APIView):
#     """"adding share to board if hash is correct"""
#     authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
#     permission_classes = (IsAuthenticated,)
#     def post(self, request, boardname):
#         user = request.auth.user
#         if request.META.get('HTTP_KBKB') == "my":
#                if 'HTTP_KBKBURL' in request.META:
#                     username = request.META.get('HTTP_KBKBURL')
#                else:
#                    HttpResponse('no user was sent with bord', status=400)
#         else:
#             HttpResponse('sharing is only allowed on private bords', status=400)
#         if 'hash' in request.DATA and 'params' in request.DATA:
#             hash = request.DATA['hash']
#             perm = request.DATA['params']
#             if checkSharedHash(user.email, boardname, username.encode(), hash.encode(), perm.encode()):
#                 boarduser = UserProfile.objects.get(username=username.encode())
#                 addPermissionToBoard(boardname, boarduser, user, perm)
#                 json_data = getBoardData(boardname, boarduser, None, None)
#                 if not json_data:
#                     return returnError('limit', 'You have reach the limit of your boards')
#                 return HttpResponse(json_data, content_type='application/json')
#             else:
#                 return HttpResponse('Bad Hash', status=401)
#         else:
#             return HttpResponse('No hash or params was sent', status=401)
#
# def addPermissionToBoard(boardname, user, newuser, perm):
#     board = get_object_or_404(Board, name=boardname, user=user)
#     perm = perm.decode("hex")
#     if perm == 'view':
#         if board.ViewUsers is not None:
#             ViewUsers = board.ViewUsers.split()
#             if not unicode(newuser.id) in ViewUsers:
#                 ViewUsers.append(unicode(newuser.id))
#                 board.ViewUsers = ' '.join(ViewUsers)
#         else:
#             board.ViewUsers = unicode(newuser.id)
#     elif perm == 'edit':
#         if board.permittedUsers is not None:
#             permittedUsers = board.permittedUsers.split()
#             if not unicode(newuser.id) in permittedUsers:
#                 permittedUsers.append(unicode(newuser.id))
#                 board.permittedUsers = ' '.join(permittedUsers)
#         else:
#             board.permittedUsers = unicode(newuser.id)
#     board.isShared = True
#     board.save()
#         #isTrue = unicode(requser.id) in permittedUsers
#
# class shareBoard(APIView):
#     authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
#     permission_classes = (IsAuthenticated, IsVerified, )
#     def post(self, request, boardname):
#         if not 'email' in request.DATA:
#             return returnError('email', 'No email was sent')
#         email = request.DATA['email'].encode()
#         if not email:
#             return returnError('email', 'Email can not be blank')
#         if not validateEmail(email):
#             return returnError('email', 'This is a bad email')
#         if not 'perm' in request.DATA:
#             return returnError('perm', 'No permission was sent')
#         perm = request.DATA['perm'].encode()
#         if not perm:
#             return returnError('perm', 'Permission can not be blank')
#         if not (perm == 'edit' or perm == 'view'):
#             return returnError('perm', 'Permission does not exists')
#
#         user = request.auth.user
#         title = "A Bord has been shared with you!"
#         tokens = "bordname="+boardname
#         correct_hash = ""
#         perm = perm.encode("hex")
#         if request.META.get('HTTP_KBKB') == "my":
#             salt = settings.SECRET_KEY
#             correct_hash = hashlib.md5(salt+boardname+user.username+salt+email+perm).hexdigest()
#             tokens += "&hash="+correct_hash+"&params="+perm
#         sendMail(user, title, "board_share", None, email, None, tokens)
#         return HttpResponse('{ "hash": "' + correct_hash + '", "params": "' + perm + '" }', content_type='application/json')
#
# def getBoardData(boardname, user, viewbords, hisuser):
#     board, created = Board.objects.get_or_create(name=boardname, user=user)
#     boardid = board.id
#     if user is not None and created:
#         if not user.isVip and user.board_count > user.maxBoards:
#             board.delete()
#             return False
#         eventRegister.objects.get_or_create(user=user, object_id=boardid)
#     if viewbords is None:
#         board.viewCount += 1
#         board.save()
#     else:
#         viewbords = viewbords.split()
#         if str(board.id) not in viewbords:
#             board.viewCount += 1
#             board.save()
#     if hisuser:
#         if hisuser.historyBoards is not None:
#             historyBoards = []
#             historyBoards = hisuser.historyBoards.split()
#             if str(board.id) in historyBoards:
#                 historyBoards.remove(str(board.id))
#             historyBoards.append(str(board.id))
#             if len(historyBoards) > 10:
#                 historyBoards.pop(0)
#             hisuser.historyBoards = ' '.join(historyBoards)
#             hisuser.save()
#         else:
#             historyBoards = []
#             historyBoards.append(str(boardid))
#             hisuser.historyBoards = ' '.join(historyBoards)
#             hisuser.save()
#     board_data = BoardSerializer(board)
#     notes = Note.objects.filter(board=boardid, isArchived=False)[:100]
#     notes_data = NoteSerializer(notes, many=True)
#     notes_json = JSONRenderer().render(notes_data.data)
#     board_json = JSONRenderer().render(board_data.data)
#     board_list = json.loads(board_json)
#     notes_list = json.loads(notes_json)
#     json_data = json.dumps({'board': board_list, 'notes': notes_list })
#     return json_data
#
# class getOrCreateBoard(APIView):
#     """Get Notes per board or create new board if not exists"""
#     authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
#     def get(self, request, boardname):
#         #boardname = boardname.encode()
#         viewbords = request.COOKIES.get('Kbkbviewbords')
#         if self.request.user.is_authenticated():
#             user = request.auth.user
#         else:
#             user = None
#         user_board = None
#         if request.META.get('HTTP_KBKB') == "my":
#             if 'HTTP_KBKBURL' in request.META:
#                 user_board = get_object_or_404(UserProfile, username=request.META.get('HTTP_KBKBURL'))
#                 if not user_board == user:
#                     board = get_object_or_401(Board, name=boardname, user=user_board)
#                     if board and isPermittedToView(board, user):
#                         pass
#                     else:
#                         return HttpResponse('Unauthorized', status=401)
#         json_data = getBoardData(boardname, user_board, viewbords, user)
#         if not json_data:
#             return returnError('limit', 'You have reach the limit of your boards')
#         return HttpResponse(json_data, content_type='application/json')
#
# class favBoard(APIView):
#     authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
#     permission_classes = (IsAuthenticated,)
#     def get(self, request, boardid):
#         user = request.auth.user
#         board_user = get_object_or_404(Board, pk=boardid).user
#         if board_user == user:
#             return HttpResponse('1', status=200)
#         if user.favBoards is not None:
#             favBoards = user.favBoards.split()
#             if unicode(boardid) not in favBoards:
#                 favBoards.append(unicode(boardid))
#             user.favBoards = ' '.join(favBoards)
#             eventRegister.objects.get_or_create(user=user, object_id=boardid)
#         else:
#             favBoards = []
#             favBoards.append(unicode(boardid))
#             user.favBoards = ' '.join(favBoards)
#         user.save()
#         return HttpResponse('0', status=200)
#
#     def delete(self, request, boardid):
#         user = request.auth.user
#         if user.favBoards is not None:
#             favBoards = user.favBoards.split()
#             if unicode(boardid) in favBoards:
#                 favBoards.remove((unicode(boardid)))
#             user.favBoards = ' '.join(favBoards)
#             eventRegister.objects.filter(user=user, object_id=boardid).delete()
#         else:
#             return HttpResponse('No Board with that id', status=404)
#         user.save()
#         user_data = UserSerializer2(user)
#         return Response(user_data.data)
#
# class BoardPatch(generics.UpdateAPIView):
#     """Delete notes by current user"""
#     authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
#     permission_classes = (IsOwner, )
#     model = Board
#     serializer_class = BoardSerializer
#
#     def patch(self, request, *args, **kwargs):
#         board = get_object_or_404(Board, pk=self.kwargs['pk'])
#         if board.isAdminBoard and not request.user.is_staff:
#             return returnError('board', 'You are not allowed to change this board')
#         return super(BoardPatch, self).patch(request, *args, **kwargs)
#
#     def post_save(self, board, *args, **kwargs):
#         if type(board.tags) is list:
#             # If tags were provided in the request
#             saved_board = Board.objects.get(pk=board.pk)
#             for tag in board.tags:
#                 saved_board.tags.add(tag)
#
# class BoardDel(generics.DestroyAPIView):
#     """Delete board by current user"""
#     authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
#     permission_classes = (IsOwner, )
#     model = Board
#     serializer_class = BoardSerializer
#     def delete(self, request, *args, **kwargs):
#         board = get_object_or_404(Board, pk=self.kwargs['pk'])
#         if board.isAdminBoard and not request.user.is_staff:
#             return returnError('board', 'You are not allowed to delete this board')
#         return super(BoardDel, self).delete(request, *args, **kwargs)
#
# class MyBoardList(generics.ListAPIView):
#     """List boards by current user"""
#     authentication_classes = (TokenAuthentication, SessionAuthentication)
#     permission_classes = (IsAuthenticated,)
#     model = Board
#     serializer_class = BoardSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if 'archived' in self.kwargs:
#             boards = Board.objects.filter(user=user, isArchived=True).order_by('-isAdminBoard', 'name')
#         else:
#             boards = Board.objects.filter(user=user, isArchived=False).order_by('-isAdminBoard', 'name')
#         if user.favBoards is not None:
#             favBoards = user.favBoards.split()
#             favBoards = Board.objects.filter(pk__in=favBoards).order_by('-isAdminBoard', 'name')
#             boards = boards | favBoards
#         return boards
#
# class MyFavBoard(generics.ListAPIView):
#     authentication_classes = (TokenAuthentication, )
#     permission_classes = (IsAuthenticated,)
#     model = Board
#     serializer_class = BoardSerializer
#
#     def get_queryset(self):
#         user = self.request.auth.user
#         favBoards = []
#         if user.favBoards is not None:
#             favBoards = user.favBoards.split()
#         return Board.objects.filter(pk__in=favBoards).order_by('name')
#
# class MyHistoryBoard(generics.ListAPIView):
#     authentication_classes = (TokenAuthentication, )
#     permission_classes = (IsAuthenticated,)
#     model = Board
#     serializer_class = BoardSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         historyBoards = []
#         if user.historyBoards is not None:
#             historyBoards = user.historyBoards.split()
#         return Board.objects.filter(pk__in=historyBoards)
#
# class HotBoards(generics.ListAPIView):
#     model = Board
#     serializer_class = NoteSerializer
#     def get(self, request):
#         notes = Note.objects.annotate(board_count=Count('board')).order_by('-board_count')[:3]
#         results = list()
#         for note in notes:
#             board = note.board
#             if board.user is None:
#                 results.append(board)
#         return HttpResponse(serializers.serialize("json", results), content_type='application/json')
#
# class BoardListSearch(generics.ListAPIView):
#     """List all files by theme"""
#     model = Board
#     serializer_class = BoardSerializer
#
#     def get_queryset(self):
#         search = self.kwargs['search']
#         if search is not None:
#             search = search.split()
#         else:
#             search = []
#         return Board.objects.filter(Q(tags__name__in=search), Q(user=None) | Q(user=self.request.user)).distinct()