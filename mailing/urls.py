from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import (
    MailingMessageListView, MailingMessageCreateView, MailingMessageUpdateView, MailingMessageDeleteView,
    MailingSettingsCreateView, MailingSettingsListView, MailingSettingsUpdateView, MailingSettingsDeleteView,
    MailingClientListView,
    ClientListView, ClientCreateView, ClientDeleteView, ClientUpdateView, toggle_client, index, MailingLogListView
)

app_name = MailingConfig.name

urlpatterns = [
    path('', index, name='index'),

    path('mailing_list/', MailingSettingsListView.as_view(), name='mailing_list'),
    path('create_mailing/', MailingSettingsCreateView.as_view(), name='create_mailing'),
    path('update_mailing/<int:pk>/', MailingSettingsUpdateView.as_view(), name='update_mailing'),
    path('delete_mailing/<int:pk>/', MailingSettingsDeleteView.as_view(), name='delete_mailing'),
    path('mailing_log/<int:pk>/', MailingLogListView.as_view(), name='mailing_log'),

    path('<int:pk>/clients', MailingClientListView.as_view(), name='mailing_clients_list'),
    path('<int:pk>/clients/add/<int:client_pk>/', toggle_client, name='mailing_clients_list_toggle'),

    path('clients/', ClientListView.as_view(), name='clients'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('message/', MailingMessageListView.as_view(), name='message'),
    path('message/create/', MailingMessageCreateView.as_view(), name='message_create'),
    path('message/update/<int:pk>/', MailingMessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', MailingMessageDeleteView.as_view(), name='message_delete'),

]

