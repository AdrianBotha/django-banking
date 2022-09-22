# Generated by Django 4.1.1 on 2022-09-19 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_banking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvimport',
            name='processed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='csvimport',
            name='processing_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_banking.processingstatus'),
        ),
    ]
