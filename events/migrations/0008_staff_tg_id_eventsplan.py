# Generated by Django 4.2.17 on 2024-12-30 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_alter_events_preferential_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='tg_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Телеграмм ID'),
        ),
        migrations.CreateModel(
            name='EventsPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('time', models.TimeField(verbose_name='Время')),
                ('comments', models.CharField(blank=True, max_length=600, null=True, verbose_name='Комментарий')),
                ('employee', models.ManyToManyField(related_name='events_plan', to='events.staff', verbose_name='Сотрудник')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events_plan', to='events.eventlist', verbose_name='Название мероприятия')),
            ],
        ),
    ]
