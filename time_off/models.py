from django.db import models
from events.models import Staff

class TimeOff(models.Model):
    employee = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='time_off', verbose_name='Сотрудник')
    date_work = models.DateField(verbose_name='Дата за которую берётся отгул')
    date_of_time_off = models.DateField(blank=True, null=True, verbose_name='Дата отгула')
    double_payment = models.BooleanField(default=False, verbose_name='Двойная оплата')
    is_closed = models.BooleanField(default=False, verbose_name='Закрытый отгул')

    def __str__(self):
        return ""
    
    class Meta:
        verbose_name = 'отгул'
        verbose_name_plural = 'Добавить отгул'
