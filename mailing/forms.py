from django import forms

from mailing.models import Client, MailingSettings, MailingMessage


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"


class MailSettingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        exclude = ('owner',)

class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = "__all__"

