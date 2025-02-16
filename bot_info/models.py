from django.db import models

class Categories(models.Model):
    category_name = models.CharField(max_length=100, verbose_name='Название категории')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории' 


class Message(models.Model):
    image = models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Изображение')
    text_message = models.TextField(verbose_name='Текст сообщения')
    categories = models.ManyToManyField(Categories, verbose_name='Категории')
    comment = models.CharField(max_length=500, blank=True, null=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки сообщения')

    def __str__(self):
        return self.text_message[:20] + "..."

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'Сообщения'


class Subscribers(models.Model):
    name = models.CharField(max_length=100, verbose_name='ФИО подписчика')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    tg_id = models.CharField(max_length=50, verbose_name='Телеграмм ID')
    categories = models.ManyToManyField(Categories, verbose_name='Категории')
    comment = models.CharField(max_length=500, blank=True, null=True, verbose_name='Комментарий')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'подписчик'
        verbose_name_plural = 'Подписчики'    

