# Generated by Django 5.1.6 on 2025-02-28 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_exittasks_date_alter_exittasks_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrytasks',
            name='date_time_add',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата, время добавления задачи'),
        ),
        migrations.AddField(
            model_name='exittasks',
            name='date_time_add',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата, время добавления задачи'),
        ),
    ]
