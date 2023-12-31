# Generated by Django 4.2.4 on 2023-08-29 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0003_mailingsettings_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingsettings',
            name='status',
            field=models.CharField(choices=[('created', 'Создано'), ('in_process', 'В процессе'), ('finished', 'Завершена')], default='created', max_length=20, verbose_name='статус'),
        ),
    ]
