from expenses.models import *
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
from django.db.models import Count
from django.contrib.auth import authenticate
from collections import OrderedDict
import re

class TagListSerializer(serializers.WritableField):

    def from_native(self, data):
        if type(data) is not list:
            raise ParseError("tags not in the right format")
        tags = []
        for tag in data:
            if type(tag) is not dict:
                raise ParseError("tag not in the right format" + str(tag))
            tags.append(tag['text'])
        return tags

    def to_native(self, obj):
        if type(obj) is not list:
            result = []
            for tag in obj.all():
                dictionary = { "text": tag.name }
                result.append(dictionary)
            return result
        return obj


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'icon_class', 'user')
        read_only_fields = ('user', )


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('name', 'category', 'icon_class', 'user')
        read_only_fields = ('user', )


class IconClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = IconClass
        fields = ('name', 'icon')


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('name', 'icon_class', 'month_balance', 'user')
        read_only_fields = ('user', )


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ('name', 'icon_class', 'account', )


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('sub_category', 'amount', 'payment_type', 'comment', 'attachment', )


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('user', 'file', )


# class UserSerializer1(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ('id', 'username', 'first_name', 'last_name', 'date_joined', 'last_login', 'city', 'country', 'punch_line')
#
# class UserSerializer2(serializers.ModelSerializer):
#     """Serializes a User object"""
#     #user = User.objects.select_related().get(pk=pk)
#     token = serializers.Field(source='auth_token.key')
#     note_count = serializers.Field(source='note_count')
#     board_count = serializers.Field(source='board_count')
#     file_count = serializers.Field(source='file_count')
#     profile_pic = serializers.Field(source='profile_pic')
#
#     class Meta:
#         model = UserProfile
#         fields = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login',
#                   'token', 'isVerified', 'profile_pic', 'note_count', 'board_count', 'file_count',
#                   'city', 'country', 'punch_line', 'maxNotes', 'maxBoards', 'maxFiles')
#         read_only_fields = ('maxNotes', 'maxBoards', 'maxFiles', 'isVerified', )
#
# class CommentSerializer(serializers.ModelSerializer):
#     user = serializers.Field(source='user.username')
#
#     class Meta:
#         model = Comment
#         fields = ('id', 'note', 'user', 'content', 'create_date', )
#
# class NoteContentSerializer(serializers.Field):
#     def field_to_native(self, obj, field_name):
#         if obj.isLocked:
#             return None
#         if obj.content:
#             return obj.content
#
#     def field_from_native(self, data, files, field_name, into):
#         if data.get('content'):
#             into['content'] = data.get('content')
#         # else:
#         #     into['content'] = self.parent.object['content']
#
# class BoardSerializer(serializers.ModelSerializer):
#     """Serializes a Note object"""
#     isSpecial = serializers.Field(source='board.isAdminBoard')
#     user = serializers.Field(source='board.user.username')
#     notesCount = serializers.Field(source='notesCount')
#     followers = serializers.Field(source='followers')
#     tags = TagListSerializer(required=False)
#     board_pic = serializers.RelatedField(many=True)
#     board_pic_cover = serializers.RelatedField(many=True)
#
#
#     class Meta:
#         model = Board
#         fields = ('id', 'name', 'user', 'isShared', 'color', 'isArchived', 'viewCount', 'tags', 'isSpecial',
#                   'notesCount', 'followers', 'isViewable', 'isPublic')
#
# class UploadedImageSerializer(serializers.ModelSerializer):
#     """Serializes a Upload Image object"""
#     user = serializers.Field(source='user.username')
#     class Meta:
#         model = UploadedImage
#         fields = ('id', 'file', 'user')
#
# class UploadedImageBoardSerializer(serializers.ModelSerializer):
#     """Serializes a Upload Image object"""
#     user = serializers.Field(source='user.username')
#     class Meta:
#         model = UploadedImageBoard
#         fields = ('id', 'file', 'user', 'board', )
#
# class UserSettingsSerializer(serializers.ModelSerializer):
#     """Serializes a user settingse object"""
#     class Meta:
#         model = UserSettings
#         fields = ('id', 'isNew', 'superString',)
#
# class UploadedFileSerializer(serializers.ModelSerializer):
#     """Serializes a Upload File object"""
#     user = serializers.Field(source='user.username')
#     url = serializers.Field(source='file.url')
#     search_url = re.search(r'\.(.*$)', str(url), re.M|re.I)
#     filename = search_url.group(0)
#
#     class Meta:
#         model = UploadedFile
#         fields = ('id', 'file', 'user', 'url', 'note')
#
# class NoteTaskSerializer(serializers.ModelSerializer):
#
#     def from_native(self, data, files):
#         locked = self.context['view'].object.isLocked
#         if locked:
#             return None
#         return data
#
#     class Meta:
#         model = NoteTask
#         fields = ('content', 'done')
#
# class NoteProgressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NoteProgress
#         fields = ('id', 'progress', 'goal', 'current')
#
# class NoteRemindersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NoteReminder
#         fields = ('id', 'schedule')
#
# class NotePollsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NotePoll
#         fields = ('id', 'poll', 'up', 'down', 'stand')
#
# class NoteFormsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NoteForm
#         fields = ('id', 'field_name', 'field_type', 'field_must')
#
# class NoteMapsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NoteMap
#         fields = ('id', 'message', 'lat', 'lng')
#
# class NoteSerializer(serializers.ModelSerializer):
#     """Serializes a Note object"""
#     user = serializers.Field(source='user.username')
#     boardname = serializers.Field(source='board.name')
#     boarduser = serializers.Field(source='board.user.username')
#     comments = CommentSerializer(required=False, many=True)
#     tags = TagListSerializer(required=False)
#     files = UploadedFileSerializer(required=False, many=True)
#     content = NoteContentSerializer()
#     tasks = NoteTaskSerializer(required=False, many=True, allow_add_remove=True, read_only=False)
#     progress = NoteProgressSerializer(required=False, many=True, allow_add_remove=True, read_only=False)
#     reminders = NoteRemindersSerializer(required=False, many=True, allow_add_remove=True, read_only=False)
#     polls = NotePollsSerializer(required=False, many=True, allow_add_remove=True, read_only=False)
#     forms = NotePollsSerializer(required=False, many=True, allow_add_remove=True, read_only=False)
#     maps = NoteMapsSerializer(required=False, many=True, allow_add_remove=True, read_only=False)
#
#     class Meta:
#         model = Note
#         fields = ('id', 'create_date', 'modify_date', 'content', 'board', 'x', 'y', 'z', 'height', 'width',
#                   'rotate', 'color', 'user', 'isMinimized', 'isArchived', 'isLighten', 'noteType', 'noteLang', 'title',
#                   'boarduser', 'boardname', 'comments', 'tags', 'files', 'isLocked', 'content', 'tasks', 'progress', 'maps', 'forms', 'polls')
#
# class TempEmailsSerializer(serializers.ModelSerializer):
#     """Serializes a temp user object"""
#     class Meta:
#         model = TempEmails
#         fields = ('email', 'isUser')
#
# class SendEmailsSerializer(serializers.ModelSerializer):
#     """Serializes a send email object"""
#     class Meta:
#         model = TempEmails
#         fields = ('user', 'note', 'tokens', 'schedule', 'recipient')
#
# class genericObjectSerializer(serializers.RelatedField):
#     def to_native(self, value):
#         """
#         Serialize bookmark instances using a bookmark serializer,
#         and note instances using a note serializer.
#         """
#         if isinstance(value, Note):
#             serializer = NoteSerializer(value)
#         elif isinstance(value, Board):
#             serializer = BoardSerializer(value)
#         elif isinstance(value, Comment):
#             serializer = CommentSerializer(value)
#         else:
#             raise Exception('Unexpected type of tagged object')
#
#         return serializer.data
#
# class historyLogSerializer(serializers.ModelSerializer):
#     """Serializes a log history object"""
#
#     user = serializers.Field(source='user.username')
#     content_type = serializers.Field(source='content_type.name')
#     content_object = genericObjectSerializer()
#
#     class Meta:
#         model = historyLog
#         fields = ('date', 'user', 'action', 'content_type', 'object_id', 'content_object')
#
# class notificationSerializer(serializers.ModelSerializer):
#     """Serializes a notification object"""
#
#     event = historyLogSerializer(required=False)
#
#     class Meta:
#         model = notification
#         fields = ('event', )
#
# class eventRegisterSerializer(serializers.ModelSerializer):
#     """Serializes a notification object"""
#
#     class Meta:
#         model = eventRegister
#         fields = ('object_id', )
#
# class AuthTokenSerializerNew(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
#
#     def validate(self, attrs):
#         username = attrs.get('username')
#         password = attrs.get('password')
#
#         if username and password:
#             if validateEmail(username):
#                 try:
#                     user = UserProfile.objects.get(email=username)
#                 except UserProfile.DoesNotExist:
#                     user = None
#                 if user is not None:
#                     username = user.username
#             user = authenticate(username=username, password=password)
#
#             if user:
#                 if not user.is_active:
#                     raise serializers.ValidationError('User account is disabled.')
#                 attrs['user'] = user
#                 return attrs
#             else:
#                 raise serializers.ValidationError('Unable to login with provided credentials.')
#         else:
#             raise serializers.ValidationError('Must include "username" and "password"')
#
# def validateEmail( email ):
#         from django.core.validators import validate_email
#         from django.core.exceptions import ValidationError
#         try:
#             validate_email( email )
#             return True
#         except ValidationError:
#             return False