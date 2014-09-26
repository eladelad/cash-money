from django.contrib import admin
from expenses.models import *

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(PaymentType)
# Register your models here.