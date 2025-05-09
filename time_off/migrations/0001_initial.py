# Generated by Django 4.2.17 on 2025-01-15 01:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0009_alter_eventsplan_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeOff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_work', models.DateField(verbose_name='Дата за которую берётся отгул')),
                ('date_of_time_off', models.DateField(blank=True, null=True, verbose_name='Дата отгула')),
                ('double_payment', models.BooleanField(default=False, verbose_name='Двойная оплата')),
                ('is_closed', models.BooleanField(default=False, verbose_name='Закрытый отгул')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_off', to='events.staff', verbose_name='Сотрудник')),
            ],
        ),
    ]
