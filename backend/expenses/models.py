from django.db import models
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from taggit.managers import TaggableManager
import reversion
import uuid
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
#from django.contrib.auth.models import AbstractUser
import datetime
import re
import ast
import os, errno
import string
import random

# Create your models here.

class GeneralObject(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, null=True, default=datetime.datetime.today())
    modify_date = models.DateTimeField(auto_now=True, null=True, default=datetime.datetime.today())
    tags = TaggableManager(blank=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.create_date = datetime.datetime.today()
        return super(GeneralObject, self).save(*args, **kwargs)


class IconClass(GeneralObject):
    name = models.CharField(max_length=150)
    icon = models.CharField(max_length=150)


def content_file_path(instance, filename):
    return '/'.join([str(instance.user.id), filename])


class Attachment(GeneralObject):
    user = models.ForeignKey(User, null=True)
    file = models.FileField(upload_to=content_file_path)

    def __unicode__(self):
        return self.user.username + " " + self.file.name


class Category(GeneralObject):
    name = models.CharField(max_length=500)
    icon_class = models.ForeignKey(IconClass)
    user = models.ForeignKey(User, null=True)


class SubCategory(GeneralObject):
    name = models.CharField(max_length=500)
    category = models.ForeignKey(Category)
    icon_class = models.ForeignKey(IconClass)
    user = models.ForeignKey(User, null=True)


class Account(GeneralObject):
    name = models.CharField(max_length=500)
    icon_class = models.ForeignKey(IconClass)
    month_balance = models.FloatField(null=False, default=0)
    user = models.ForeignKey(User, null=True)


class PaymentType(GeneralObject):
    name = models.CharField(max_length=500)
    icon_class = models.ForeignKey(IconClass)
    account = models.ForeignKey(Account)


class Transaction(GeneralObject):
    sub_category = models.ForeignKey(SubCategory)
    amount = models.FloatField(default=0)
    payment_type = models.ForeignKey(PaymentType)
    comment = models.CharField(max_length=500, null=True)
    attachment = models.ForeignKey(Attachment)





# class Board(MokoObject):
#     name = models.CharField(max_length=100)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, null=True, default=None)
#     color = models.CharField(max_length=7, default="#ffffff")
#     isShared = models.BooleanField(default=False)
#     isPublic = models.BooleanField(default=False)
#     isArchived = models.BooleanField(default=False)
#     isViewable = models.BooleanField(default=False)
#     viewCount = models.IntegerField(default=0)
#     permittedUsers = models.TextField(null=True, blank=True)
#     ViewUsers = models.TextField(null=True, blank=True)
#     isAdminBoard = models.BooleanField(default=False)
#
#     def notesCount(self):
#         return Note.objects.filter(board=self.id, isArchived=False).count()
#
#     def followers(self):
#         if self.permittedUsers is not None:
#             permittedUsers = self.permittedUsers.split()
#             return len(permittedUsers)
#         return 0
#
#     def save(self, *args, **kwargs):
#         if not self.permittedUsers:
#             self.permittedUsers = None
#         super(Board, self).save(*args, **kwargs)
#
#     def __unicode__(self):
#         return self.name
#
# class Note(MokoObject):
#     content = models.TextField(default="")
#     board = models.ForeignKey(Board)
#     x = models.IntegerField(default=0)
#     y = models.IntegerField(default=-100)
#     z = models.IntegerField(default=0)
#     rotate = models.IntegerField(default=0)
#     height = models.IntegerField(default=300)
#     width = models.IntegerField(default=300)
#     color = models.CharField(max_length=7, default="#ffffff")
#     title = models.TextField(null=True, blank=True)
#     isMinimized = models.BooleanField(default=False)
#     isArchived = models.BooleanField(default=False)
#     isLighten = models.BooleanField(default=False)
#     isLocked = models.BooleanField(default=False)
#     noteType = models.CharField(max_length=500, default="HTML")
#     noteLang = models.CharField(max_length=100, default="EN")
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, null=True)
#
#
#     def __unicode__(self):
#         if self.board.name is None:
#             return str(self.id) + " Null Board Name"
#         else:
#             return str(self.id) + " " + str(self.board.name)
#
# reversion.register(Note, fields=["content", "isLocked", "board", "noteLang"])
#
# class Comment(MokoObject):
#     note = models.ForeignKey(Note, related_name='comments')
#     content = models.TextField(default="")
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, blank=True)
#
#     def __unicode__(self):
#         return '%s %s' % (self.user.username, self.content)
#
# class NoteTask(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, default=None, null=True)
#     note = models.ForeignKey(Note, related_name='tasks')
#     content = models.CharField(null=True, blank=True, default=None, max_length=500)
#     done = models.BooleanField(default=False)
#
#     def __unicode__(self):
#         return '%s %s %s' % (self.note.title, self.content, self.id)
#
#     class Meta:
#         ordering = ['id']
#
# class NoteProgress(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, default=None, null=True)
#     note = models.ForeignKey(Note, related_name='progress')
#     progress = models.CharField(null=True, blank=True, default=None, max_length=500)
#     goal = models.IntegerField(default=100, null=False)
#     current = models.IntegerField(default=0, null=False)
#
#     def __unicode__(self):
#         return '%s %s %s' % (self.note.title, self.content, self.id)
#
#     class Meta:
#         ordering = ['id']
#
# class NoteReminder(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, default=None, null=True)
#     note = models.ForeignKey(Note, related_name='reminders')
#     schedule = models.DateTimeField(default=datetime.datetime.today())
#
#     def __unicode__(self):
#         return '%s %s %s' % (self.note.title, self.content, self.id)
#
#     class Meta:
#         ordering = ['id']
#
# class NotePoll(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, default=None, null=True)
#     note = models.ForeignKey(Note, related_name='polls')
#     poll = models.CharField(null=True, blank=True, default=None, max_length=500)
#     up = models.IntegerField(default=0, null=False)
#     down = models.IntegerField(default=0, null=False)
#     stand = models.IntegerField(default=0, null=False)
#
#     def __unicode__(self):
#         return '%s %s %s' % (self.note.title, self.content, self.id)
#
#     class Meta:
#         ordering = ['id']
#
#
# class NoteForm(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, default=None, null=True)
#     note = models.ForeignKey(Note, related_name='forms')
#     field_name = models.CharField(null=True, blank=True, default=None, max_length=500)
#     field_type = models.CharField(null=True, blank=True, default=None, max_length=500)
#     field_must = models.BooleanField(default=False)
#
#     def __unicode__(self):
#         return '%s %s %s' % (self.note.title, self.content, self.id)
#
#     class Meta:
#         ordering = ['id']
#
# class NoteMap(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, default=None, null=True)
#     note = models.ForeignKey(Note, related_name='maps')
#     message = models.CharField(null=True, blank=True, default=None, max_length=500)
#     lat = models.FloatField(null=False, default=0)
#     lng = models.FloatField(null=False, default=0)
#
#     def __unicode__(self):
#         return '%s %s %s' % (self.note.title, self.content, self.id)
#
#     class Meta:
#         ordering = ['id']
#
# class UploadedImage(MokoObject):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, null=True, related_name='profile_pic')
#     file = models.ImageField(upload_to=content_file_path_profile)
#
#     def __unicode__(self):
#         return self.user.username + " " + self.file.name
#
# class UploadedImageBoard(MokoObject):
#     board = models.ForeignKey(Board, editable=False, null=True, related_name='board_pic')
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, null=True)
#     file = models.ImageField(upload_to=content_file_path_board)
#
# class UploadedImageBoardCover(MokoObject):
#     board = models.ForeignKey(Board, editable=False, null=True, related_name='board_pic_cover')
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, null=True)
#     file = models.ImageField(upload_to=content_file_path_board_cover)
#
# class UploadedFile(MokoObject):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, null=True)
#     note = models.ForeignKey(Note, null=True, related_name='files')
#     file = models.FileField(upload_to=content_file_path)
#
#     def __unicode__(self):
#         return self.user.username + " " + self.file.name
#
# class UserSettings(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)
#     isNew = models.BooleanField(default=True)
#     superString = models.TextField(blank=True, default="")
#     notifyByMail = models.BooleanField(default=True)
#
#     def __unicode__(self):
#         return self.user.username
#
# class UserProfile(AbstractUser):
#     city = models.CharField(null=True, default=None, blank=True, max_length=200)
#     country = models.CharField(null=True, default=None, blank=True, max_length=200)
#     punch_line = models.CharField(null=True, default=None, blank=True, max_length=250)
#     phone = models.BigIntegerField(null=True, default=None, blank=True, max_length=13)
#     favBoards = models.TextField(null=True, default=None, blank=True)
#     historyBoards = models.TextField(null=True, default=None, blank=True)
#     isVerified = models.BooleanField(default=False)
#     isVip = models.BooleanField(default=False)
#     maxNotes = models.IntegerField(default=200)
#     maxBoards = models.IntegerField(default=10)
#     maxFiles = models.IntegerField(default=40)
#
#     def profile_pic(self):
#         return UploadedImage.objects.filter(user=self).order_by('-modify_date')[0]
#
#     def note_count(self):
#         return Note.objects.filter(user=self, isArchived=False).count()
#
#     def board_count(self):
#         return Board.objects.filter(user=self).count()
#
#     def file_count(self):
#         return UploadedFile.objects.filter(user=self).count()
#
#     def save(self, *args, **kwargs):
#         if not self.favBoards:
#             self.favBoards = None
#         if not self.historyBoards:
#             self.historyBoards = None
#         if not self.profile_pic:
#             self.profile_pic = None
#
#         super(UserProfile, self).save(*args, **kwargs)
#
# class TempEmails(MokoObject):
#     email = models.EmailField(unique=True)
#     isUser = models.BooleanField(default=False)
#
#     def __unicode__(self):
#         return self.email
#
# class sendEmails(MokoObject):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL)
#     note = models.ForeignKey(Note, null=True)
#     title = models.CharField(max_length=250, default="Email From KlipBord")
#     message = models.CharField(max_length=100, default="default")
#     tokens = models.TextField(null=True, blank=True)
#     schedule = models.DateTimeField(default=datetime.datetime.today())
#     recipient = models.EmailField()
#     isSent = models.BooleanField(default=False)
#
#     def save(self, *args, **kwargs):
#         if not self.tokens:
#             self.tokens = None
#         super(sendEmails, self).save(*args, **kwargs)
#
#     def __unicode__(self):
#         return self.user.email + " " + self.recipient + " " + self.message
#
# class miniHash(models.Model):
#     minihash = models.CharField(max_length=8, default="")
#     email = models.EmailField()
#
#     def save(self, *args, **kwargs):
#         self.minihash = id_generator()
#         super(miniHash, self).save(*args, **kwargs)
#
# class historyLog(models.Model):
#
#     ACTION_CHOICES = (
#         ('NEW', 'Created a new'),
#         ('MOD', 'Modified'),
#         ('DEL', 'Deleted'),
#     )
#
#     date = models.DateTimeField(auto_now_add=True, null=True, default=datetime.datetime.today())
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
#     action = models.CharField(max_length=3, choices=ACTION_CHOICES, default='NEW')
#     content_type = models.ForeignKey(ContentType, null=True, blank=True)
#     object_id = models.PositiveIntegerField(null=True, blank=True)
#     content_object = GenericForeignKey('content_type', 'object_id')
#
#     def __unicode__(self):
#         user = 'Anonymous'
#         if self.user:
#             user = self.user.username
#         action = self.get_action_display()
#         return " ".join([str(self.date), user, action, self.content_type.name, str(self.object_id)])
#
# class eventRegister(models.Model):
#
#     user = models.ForeignKey(settings.AUTH_USER_MODEL)
#     object_id = models.PositiveIntegerField(default=0)
#
#     def __unicode__(self):
#         return " ".join([self.user.username, str(self.object_id)])
#
# class notification(models.Model):
#     date = models.DateTimeField(auto_now_add=True, null=True, default=datetime.datetime.today())
#     user = models.ForeignKey(settings.AUTH_USER_MODEL)
#     event = models.ForeignKey(historyLog)
#     isRead = models.BooleanField(default=False)
#     isSent = models.BooleanField(default=False)
#
#     def __unicode__(self):
#         return " ".join([self.user.username, self.event.content_type.name, str(self.event.content_object.id)])
#
#
# post_save.connect(logItSave, sender=Note, dispatch_uid=str(uuid.uuid1()))
# post_delete.connect(logItDelete, sender=Note, dispatch_uid=str(uuid.uuid1()))
# # post_save.connect(logItSave, sender=Board, dispatch_uid=str(uuid.uuid1()))
# # post_delete.connect(logItDelete, sender=Board, dispatch_uid=str(uuid.uuid1()))
# post_save.connect(logItSave, sender=Comment, dispatch_uid=str(uuid.uuid1()))
# post_delete.connect(logItDelete, sender=Comment, dispatch_uid=str(uuid.uuid1()))
# post_save.connect(logItSave, sender=UploadedFile, dispatch_uid=str(uuid.uuid1()))
# post_delete.connect(logItDelete, sender=UploadedFile, dispatch_uid=str(uuid.uuid1()))
# post_save.connect(logItSave, sender=sendEmails, dispatch_uid=str(uuid.uuid1()))