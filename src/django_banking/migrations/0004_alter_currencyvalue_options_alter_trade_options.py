# Generated by Django 4.1.1 on 2022-09-20 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_banking', '0003_rename_slug_currency_iso_code_currencyvalue'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currencyvalue',
            options={'ordering': ['day', 'currency']},
        ),
        migrations.AlterModelOptions(
            name='trade',
            options={'ordering': ['date']},
        ),
    ]