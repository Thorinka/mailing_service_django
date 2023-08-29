from django.conf import settings
from django.db import models

# Create your models here.

NULLABLE = {
    'blank': True,
    'null': True
}


class Client(models.Model):
    email = models.EmailField(verbose_name='email')
    client_name = models.CharField(max_length=150, verbose_name='фио')
    comment = models.TextField(verbose_name='комментарий')

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class MailingMessage(models.Model):
    subject = models.CharField(max_length=50, verbose_name='тема')
    text = models.TextField(verbose_name='текст')

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'cooбщения'


class MailingSettings(models.Model):
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'

    PERIODS = (
        (PERIOD_DAILY, 'Ежедневно'),
        (PERIOD_WEEKLY, 'Еженедельно'),
        (PERIOD_MONTHLY, 'Ежемесячно'),
    )

    STATUS_CREATED = 'created'
    STATUS_IN_PROCESS = 'in_process'
    STATUS_FINISHED = 'finished'

    STATUSES = (
        (STATUS_CREATED, 'Создано'),
        (STATUS_IN_PROCESS, 'В процессе'),
        (STATUS_FINISHED, 'Завершена'),
    )

    start_time = models.DateTimeField(verbose_name='время начала')
    end_time = models.DateTimeField(verbose_name='время окончания', **NULLABLE)
    period = models.CharField(max_length=20, choices=PERIODS, default=PERIOD_DAILY, verbose_name='период')
    status = models.CharField(max_length=20, choices=STATUSES, default=STATUS_CREATED, verbose_name='статус')

    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE, verbose_name='сообщение')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return f'{self.start_time} / {self.period}'

    class Meta:
        verbose_name = 'настройка'
        verbose_name_plural = 'настройки'



class MailingClient(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент')
    settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='настройки')

    def __str__(self):
        return f'{self.client} / {self.settings}'

    class Meta:
        verbose_name = 'клиент рассылки'
        verbose_name_plural = 'клиенты рассылки'


class MailingLog(models.Model):
    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'
    STATUSES = (
        (STATUS_SUCCESS, 'Успешно'),
        (STATUS_FAILED, 'Ошибка'),
    )

    last_try = models.DateTimeField(auto_now_add=True, verbose_name='дата последней попытки')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент')
    settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='настройки')
    status = models.CharField(choices=STATUSES, default=STATUS_SUCCESS, verbose_name='статус')
    mail_service_response = models.TextField(**NULLABLE, verbose_name='ответ почтового сервиса')

    def __str__(self):
        return f'{self.last_try}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
