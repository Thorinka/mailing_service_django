import datetime
import random

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import request
from django.shortcuts import render

from blog.models import Blog
from mailing.models import MailingLog, MailingSettings, Client


def send_email(message_settings, message_client):
    try:
        result = send_mail(
            subject=message_settings.message.subject,
            message=message_settings.message.text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[message_client.client.email],
            fail_silently=False
        )

        MailingLog.objects.create(
            status=MailingLog.STATUS_SUCCESS if result else MailingLog.STATUS_FAILED,
            settings=message_settings,
            client_id=message_client.client_id,
            mail_service_response='OK'
        )
    except Exception:
        MailingLog.objects.create(
            status=MailingLog.STATUS_SUCCESS if result else MailingLog.STATUS_FAILED,
            settings=message_settings,
            client_id=message_client.client_id,
            mail_service_response='error'
        )


def send_mails():
    datetime_now = datetime.datetime.now(datetime.timezone.utc)
    for mailing_setting in MailingSettings.objects.filter(status=MailingSettings.STATUS_IN_PROCESS):

        if (datetime_now > mailing_setting.start_time) and (datetime_now < mailing_setting.end_time):

            for mailing_client in mailing_setting.mailingclient_set.all():

                mailing_log = MailingLog.objects.filter(
                    client=mailing_client.client,
                    settings=mailing_setting
                )

                if mailing_log.exists():
                    last_try_date = mailing_log.order_by('-last_try').first().last_try
                    mailing_period = mailing_log[0]

                    if mailing_period == MailingSettings.PERIOD_DAILY:
                        if (datetime_now - last_try_date).days >= 1:
                            send_email(mailing_setting, mailing_client)
                    elif mailing_period == MailingSettings.PERIOD_WEEKLY:
                        if (datetime_now - last_try_date).days >= 7:
                            send_email(mailing_setting, mailing_client)
                    elif mailing_period == MailingSettings.PERIOD_MONTHLY:
                        if (datetime_now - last_try_date).days >= 30:
                            send_email(mailing_setting, mailing_client)
                    else:
                        send_email(mailing_setting, mailing_client)


def get_random_blog():
    items = list(Blog.objects.all())
    if len(items) < 3:
        random_items = random.sample(items, len(items))
    else:
        random_items = random.sample(items, 3)
    return random_items


def get_cached_data():
    if settings.CACHE_ENABLED:
        key_total_mailings_counter = 'total_mailings_counter'
        key_active_mailings_counter = 'active_mailings_counter'
        key_unique_client_counter = 'unique_client_counter'

        total_mailings_counter = cache.get(key_total_mailings_counter)
        active_mailings_counter = cache.get(key_active_mailings_counter)
        unique_client_counter = cache.get(key_unique_client_counter)

        if total_mailings_counter is None:
            total_mailings_counter = MailingSettings.objects.all()
            cache.get(key_total_mailings_counter, total_mailings_counter)
        else:
            total_mailings_counter = MailingSettings.objects.all()

        if active_mailings_counter is None:
            active_mailings_counter = MailingSettings.objects.filter(status=MailingSettings.STATUS_IN_PROCESS)
            cache.get(key_active_mailings_counter, active_mailings_counter)
        else:
            total_mailings_counter = MailingSettings.objects.filter(status=MailingSettings.STATUS_IN_PROCESS)

        if unique_client_counter is None:
            unique_client_counter = Client.objects.all().distinct('email')
            cache.get(key_unique_client_counter, unique_client_counter)
        else:
            unique_client_counter = Client.objects.all().distinct('email')

        return total_mailings_counter, active_mailings_counter, unique_client_counter
