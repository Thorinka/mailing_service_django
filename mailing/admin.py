from django.contrib import admin

from mailing.models import Client, MailingSettings, MailingMessage


# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'client_name',)
    list_filter = ('email', 'client_name',)
    search_fields = ('email', 'client_name',)


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'period', 'status',)
    list_filter = ('start_time', 'status',)
    search_fields = ('start_time', 'period',)


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject',)
    list_filter = ('subject',)
    search_fields = ('subject', 'text',)
