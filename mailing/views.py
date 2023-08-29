import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from blog.models import Blog
from mailing.forms import MailSettingsForm, ClientForm, MessageForm
from mailing.models import MailingSettings, Client, MailingClient, MailingMessage, MailingLog
from mailing.services import get_random_blog, get_cached_data


# Settings

class MailingSettingsListView(LoginRequiredMixin, ListView):
    model = MailingSettings

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_staff:
            queryset = super().get_queryset().filter(owner=self.request.user)

        return queryset


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    form_class = MailSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class MailingSettingsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MailingSettings
    form_class = MailSettingsForm
    permission_required = 'mailing.change_mailingsettings'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404

        return self.object


class MailingSettingsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MailingSettings
    permission_required = 'mailing.delete_mailingsettings'
    success_url = reverse_lazy('mailing:mailing_list')


# Mail+Client


class MailingClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MailingClient
    permission_required = 'mailing.view_mailingclient'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['clients'] = Client.objects.all()
        context_data['mailing_pk'] = self.kwargs.get('pk')

        return context_data


# Client


class ClientListView(LoginRequiredMixin, ListView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients')


# Message

class MailingMessageListView(LoginRequiredMixin, ListView):
    model = MailingMessage


class MailingMessageCreateView(LoginRequiredMixin, CreateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message')


class MailingMessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MailingMessage
    form_class = MessageForm
    permission_required = 'mailing.change_mailingmessage'
    success_url = reverse_lazy('mailing:message')


class MailingMessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MailingMessage
    permission_required = 'mailing.delete_mailingsettings'
    success_url = reverse_lazy('mailing:message')


class MailingLogListView(LoginRequiredMixin, ListView):
    model = MailingLog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = MailingLog.objects.filter(settings=self.kwargs.get('pk')).order_by('-last_try')
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['settings'] = MailingSettings.objects.get(pk=self.kwargs.get('pk'))
        return context_data


@login_required
def toggle_client(request, pk, client_pk):
    if MailingClient.objects.filter(
            client_id=client_pk,
            settings_id=pk
    ).exists():
        MailingClient.objects.filter(client_id=client_pk, settings_id=pk).delete()
    else:
        MailingClient.objects.create(client_id=client_pk, settings_id=pk)

    return redirect(reverse('mailing:mailing_clients_list', args=[pk]))


def index(request):
    total_mailings_counter, active_mailings_counter, unique_client_counter = get_cached_data()
    context = {
        'title': 'Главная',
        'total_mailings_counter': len(total_mailings_counter),
        'active_mailing_counter': len(active_mailings_counter),
        'unique_client_counter': len(unique_client_counter),
        'random_blog': get_random_blog(),
    }
    return render(request, 'mailing/index.html', context)


# def random_blogs(request):
#     items = list(Blog.objects.all())
#     random_items = random.sample(items, 3)
#     return render(request, 'news/posts.html', {'random_article': random_items})
