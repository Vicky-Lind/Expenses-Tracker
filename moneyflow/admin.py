from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Account, Category, Document, Transaction


@admin.register(Document)
class DocumentAdmin(ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    pass


@admin.register(Account)
class AccountAdmin(ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    pass
