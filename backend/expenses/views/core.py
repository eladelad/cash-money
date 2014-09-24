from notes.models import *
from notes.serializers import *
#from notes.permissions import * #can't import

from taggit.models import Tag

from app.models import *
from app.serializers import *
import hashlib
from simplecrypt import encrypt, decrypt
from simplecrypt import DecryptionException
import itertools
import base64

import os
import json
import datetime
from itertools import chain

from django.core import serializers
from django.utils import timezone
from rest_framework.renderers import JSONRenderer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.shortcuts import get_object_or_401

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def returnError(field, text):
    error = {}
    error[field] = []
    error[field].append(text)
    return HttpResponse(json.dumps(error), content_type='application/json', status=400)

def isPermittedToEdit(board, user):
    if user is not None and user.is_staff:
        return True
    if board.user == user or board.user is None or board.isPublic:
        return True
    if board.isAdminBoard:
        return False
    elif user is None:
        return False

    if board.permittedUsers is not None:
        permittedUsers = board.permittedUsers.split()
        return unicode(user.id) in permittedUsers
    else:
        return False

def isPermittedToView(board, user):
    if isPermittedToEdit(board, user):
        return True
    if board.isViewable:
        return True
    if user is not None and board.ViewUsers is not None:
        ViewUsers = board.ViewUsers.split()
        return unicode(user.id) in ViewUsers


def checkSharedHash(email, board, username, hash, perm):
    salt = settings.SECRET_KEY
    #correcthash = hashlib.md5(salt+board+username+salt+email+perm).hexdigest()
    return hash == hashlib.md5(salt+board+username+salt+email+perm).hexdigest()

def createHash(email):
    salt = settings.SECRET_KEY
    return hashlib.md5(salt+email+salt).hexdigest()

def checkHash(hash):
    minihash = hash[0:8]
    hash = hash[8:len(hash)]
    email = miniHash.objects.get(minihash=minihash)
    if email:
        if createHash(email.email) == hash:
            return email.email
    return False

def validateEmail( email ):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def sendMail(user, title, message, note, recipient, schedule, tokens):
    #if isinstance( note, ( int, long ):
    if schedule is None:
        schedule = datetime.datetime.now(tz=timezone.get_current_timezone())
    mail = sendEmails(user=user, note=note, title=title, message=message, recipient=recipient,
                      schedule=schedule, tokens=tokens)
    mail.save()

class AdminSendEmail(generics.CreateAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAdminUser,)
    model = sendEmails
    serializer_class = SendEmailsSerializer

def makeMiniHash(email):
    minihash = miniHash.objects.get_or_create(email=email)
    return minihash[0].minihash

class GeneralListSearch(APIView):
    """List all files by theme"""
    def get(self, request, search):
        if search is not None:
            search = search.split()
            boards = Board.objects.filter(tags__name__in=search).distinct()
            notes = Note.objects.filter(tags__name__in=search).distinct()
            boards_serializer = BoardSerializer(boards, many=True)
            notes_serializer = NoteSerializer(notes, many=True)
            notes_json = JSONRenderer().render(notes_serializer.data)
            board_json = JSONRenderer().render(boards_serializer.data)
            board_list = json.loads(board_json)
            notes_list = json.loads(notes_json)
            json_data = json.dumps({'boards': board_list, 'notes': notes_list })
            return HttpResponse(json_data, content_type='application/json')
        else:
            return returnError('search', 'Search is empty')

def get_dir_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def list_tags(request):
    max_results = getattr(settings, 'MAX_NUMBER_OF_RESULTS', 100)
    try:
        tags = [{'id': tag.id, 'label': tag.name, 'text': tag.name}
                for tag in Tag.objects.filter(name__istartswith=request.GET['q'])[:max_results]]
    except MultiValueDictKeyError:
        raise Http404

    return HttpResponse(json.dumps(tags), content_type='application/json')

def encrypt_content(content, key):
    salt = settings.SECRET_KEY
    secret = hashlib.md5(key + salt).hexdigest()
    # simple crypt save in bytes so convert to base 64
    # http://stackoverflow.com/questions/7214426/save-byte-string-to-varchar-column-in-database
    #content = base64.b64encode(encrypt(secret, content))
    return base64.b64encode(encrypt(secret, content.encode('utf8')))
    return content

def decrypt_content(content, key):
    salt = settings.SECRET_KEY
    secret = hashlib.md5(key + salt).hexdigest()
    try:
        content = decrypt(secret, base64.b64decode(content))
    except DecryptionException:
        content = False
    return content

def limit_user(user, model):
    if model == 'note' and user.note_count + 1 > user.maxNotes:
        return False
    if model == 'board' and user.board_count + 1 > user.maxBoards:
        return False
    if model == 'file' and user.file_count + 1 > user.maxFiles:
        return False
    return True

class Counters(APIView):
    def get(self,request):
        note_count = Note.objects.filter().count()
        board_count = Board.objects.filter().count()
        file_count = UploadedFile.objects.filter().count()
        result = {}
        result['notes'] = note_count
        result['boards'] = board_count
        result['files'] = file_count
        return HttpResponse(json.dumps(result), content_type='application/json')