from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('tx_ref', 'user', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('tx_ref', 'user__email', 'organization__name')
    readonly_fields = ('tx_ref', 'amount', 'currency', 'created_at')