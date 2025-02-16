from django.db import models
from django.core.exceptions import ValidationError


class Staff(models.Model):
    name = models.CharField(max_length=50, verbose_name='ФИО сотрудника')
    role = models.CharField(max_length=50, verbose_name='Должность')
    actual = models.BooleanField(default=True, verbose_name='Действующий сотрудник')
    tg_id = models.CharField(max_length=50, verbose_name='Телеграмм ID', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'сотрудника'
        verbose_name_plural = 'Сотрудники музея'


class Location(models.Model):
    location = models.CharField(max_length=50, verbose_name='Место проведения')

    def __str__(self):
        return self.location

    class Meta:
        verbose_name = 'место проведения'
        verbose_name_plural = 'Место проведения'


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория мероприятия')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категорию мероприятия'
        verbose_name_plural = 'Категории мероприятий'


class FreeOrNot(models.Model):
    free_or_not = models.CharField(max_length=50, verbose_name='Платно или бесплатно')

    def __str__(self):
        return self.free_or_not

    class Meta:
        verbose_name = 'платно или нет'
        verbose_name_plural = 'Платно или нет'


class EventList(models.Model):
    event_name = models.CharField(max_length=100, verbose_name='Название мероприятия')
    date_start_event = models.DateField(blank=True, null=True, verbose_name='Дата начала')
    date_end_event = models.DateField(blank=True, null=True, verbose_name='Дата окончания')

    def clean(self):
        if self.date_start_event and self.date_end_event:
            if self.date_end_event < self.date_start_event:
                raise ValidationError('Дата окончания события не может быть больше даты начала')
            
    def __str__(self):
        return self.event_name
    
    class Meta:
        verbose_name = 'мероприятие'
        verbose_name_plural = 'Список возможных мероприятий'
    
class Events(models.Model):
    date = models.DateField(verbose_name='Дата')
    employee = models.ManyToManyField(Staff, related_name='events', verbose_name='Сотрудник')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='events', verbose_name='Место проведения')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='events', verbose_name='Категория мероприятия')
    event_name = models.ForeignKey(EventList, on_delete=models.CASCADE, related_name='events', verbose_name='Название мероприятия')

    region = models.CharField(max_length=100, blank=True, null=True, verbose_name='Регион или страна')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')

    VPN = models.PositiveIntegerField(verbose_name='ВПН', default=0)
    adults = models.PositiveIntegerField(verbose_name='Взрослые', default=0)
    university_students = models.PositiveIntegerField(verbose_name='Студенты ВУЗ', default=0)
    college_students = models.PositiveIntegerField(verbose_name='Студенты колледж', default=0)
    school = models.PositiveIntegerField(verbose_name='Школьники', default=0)
    children = models.PositiveIntegerField(verbose_name='Докольники', default=0)
    pensioners = models.PositiveIntegerField(verbose_name='Пенсионеры', default=0)

    socially_supported_children = models.PositiveIntegerField(verbose_name='Социально опекаемые дети', default=0)
    socially_supported_adult = models.PositiveIntegerField(verbose_name='Взрослые', default=0)
    pushkn_cards = models.PositiveIntegerField(verbose_name='Пушкинская карта', default=0)
    indigenous_children = models.PositiveIntegerField(verbose_name='Дети КМНС', default=0)
    indigenous_adult = models.PositiveIntegerField(verbose_name='Взрослые КМНС', default=0)
    autism_spectrum_children = models.PositiveIntegerField(verbose_name='РАС', default=0)
    svo_children = models.PositiveIntegerField(verbose_name='Дети участников СВО', default=0)
    
    preferential = models.PositiveIntegerField(verbose_name='Льготно', default=0)
    free_or_not = models.ForeignKey(FreeOrNot, on_delete=models.CASCADE, null=True, verbose_name='Платно или нет')
    feedback = models.BooleanField(default=False, verbose_name='Положительный отзыв')
    Comments = models.CharField(max_length=600, verbose_name='Комментарий', blank=True, null=True)

    class Meta:
        verbose_name = 'путёвку'
        verbose_name_plural = 'Путёвки'

    def __str__(self):
        return ""
    
class FreeVisitors(models.Model):
    date = models.DateField(verbose_name='Дата')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='free_visitors', verbose_name='Место проведения')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='free_visitors', verbose_name='Категория мероприятия')
    event_name = models.ForeignKey(EventList, on_delete=models.CASCADE, related_name='free_visitors', verbose_name='Название мероприятия')

    region = models.CharField(max_length=100, blank=True, null=True, verbose_name='Регион или страна')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')

    VPN = models.PositiveIntegerField(verbose_name='ВПН', default=0)
    adults = models.PositiveIntegerField(verbose_name='Взрослые', default=0)
    university_students = models.PositiveIntegerField(verbose_name='Студенты ВУЗ', default=0)
    college_students = models.PositiveIntegerField(verbose_name='Студенты колледж', default=0)
    school = models.PositiveIntegerField(verbose_name='Школьники', default=0)
    children = models.PositiveIntegerField(verbose_name='Докольники', default=0)
    pensioners = models.PositiveIntegerField(verbose_name='Пенсионеры', default=0)

    socially_supported_children = models.PositiveIntegerField(verbose_name='Социально опекаемые дети', default=0)
    socially_supported_adult = models.PositiveIntegerField(verbose_name='Взрослые', default=0)
    pushkn_cards = models.PositiveIntegerField(verbose_name='Пушкинская карта', default=0)
    indigenous_children = models.PositiveIntegerField(verbose_name='Дети КМНС', default=0)
    indigenous_adult = models.PositiveIntegerField(verbose_name='Взрослые КМНС', default=0)
    autism_spectrum_children = models.PositiveIntegerField(verbose_name='РАС', default=0)
    svo_children = models.PositiveIntegerField(verbose_name='Дети участников СВО', default=0)
    
    preferential = models.PositiveIntegerField(verbose_name='Льготно', default=0)
    free_or_not = models.ForeignKey(FreeOrNot, on_delete=models.CASCADE, null=True, verbose_name='Платно или нет')
    feedback = models.BooleanField(default=False, verbose_name='Положительный отзыв')
    Comments = models.CharField(max_length=600, verbose_name='Комментарий', blank=True, null=True)

    class Meta:
        verbose_name = 'индивидуальные посетители'
        verbose_name_plural = 'Индивидуальные посетители'

    def __str__(self):
        return ""
    
class EventsPlan(models.Model):
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    employee = models.ManyToManyField(Staff, related_name='events_plan', verbose_name='Сотрудник')
    event = models.ForeignKey(EventList, on_delete=models.CASCADE, related_name='events_plan', verbose_name='Название мероприятия')
    comments = models.CharField(max_length=600, verbose_name='Комментарий', blank=True, null=True)

    class Meta:
        verbose_name = 'событие'
        verbose_name_plural = 'Занятость сотрудников'

    def __str__(self):
        return ""