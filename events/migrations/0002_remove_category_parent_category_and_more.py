# Generated by Django 4.2.17 on 2024-12-07 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent_category',
        ),
        migrations.AlterField(
            model_name='events',
            name='Comments',
            field=models.CharField(blank=True, max_length=600, null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='events',
            name='preferential',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Льготно'),
        ),
    ]
