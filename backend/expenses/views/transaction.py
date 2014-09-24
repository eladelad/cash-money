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

class Transaction(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)