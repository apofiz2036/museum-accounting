# Generated by Django 4.2.17 on 2024-12-07 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_remove_category_parent_category_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'категория мероприятия', 'verbose_name_plural': 'Категории мероприятий'},
        ),
        migrations.AlterModelOptions(
            name='eventlist',
            options={'verbose_name': 'мероприятие', 'verbose_name_plural': 'Список возможных мероприятий'},
        ),
        migrations.AlterModelOptions(
            name='events',
            options={'verbose_name': 'путёвка', 'verbose_name_plural': 'Путёвки'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'место проведения', 'verbose_name_plural': 'Место проведения'},
        ),
        migrations.AlterModelOptions(
            name='staff',
            options={'verbose_name': 'сотрудник', 'verbose_name_plural': 'Сотрудники музея'},
        ),
    ]
