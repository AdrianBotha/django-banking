# Generated by Django 4.1.1 on 2022-09-20 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_banking', '0002_alter_csvimport_processed_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='currency',
            old_name='slug',
            new_name='iso_code',
        ),
        migrations.CreateModel(
            name='CurrencyValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('rate', models.FloatField()),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_banking.currency')),
            ],
        ),
    ]