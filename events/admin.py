from django.contrib import admin
from django.contrib.auth.models import Group, User
from time_off.models import TimeOff
from bot_info.models import Categories, Message, Subscribers
from .models import Staff, Location, Category, EventList, Events, FreeVisitors, FreeOrNot, EventsPlan
from .forms import EventForm
from django.utils import formats


class TimeOffAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date_work', 'date_of_time_off', 'double_payment', 'is_closed')
    list_filter = ('employee', 'double_payment', 'is_closed')

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category_name',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('text_message', 'created_at')

class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number')

class StaffAdmin(admin.ModelAdmin): 
    list_display = ('name', 'role', 'actual')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('location',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class EventListAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'date_start_event', 'date_end_event')
    search_fields = ('event_name',) 

class EventsAdmin(admin.ModelAdmin):
    list_display = ('date', 'first_employee', 'location', 'event_name', 'Comments')
    list_filter = ('date', 'employee', 'location', 'event_name', 'category')
    autocomplete_fields = ['event_name']

    def first_employee(self, obj):
        if obj.employee.exists():
            return obj.employee.first().name
        return 'Сотрудник удалён'
    
    first_employee.short_description = 'Сотрудник'
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "employee":
            kwargs["queryset"] = Staff.objects.filter(actual=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
class FreeVisitorsAdmin(admin.ModelAdmin):
    list_display = ('date', 'location', 'event_name', 'Comments')

class FreeOrNotAdmin(admin.ModelAdmin):
    list_display = ('free_or_not',)

class EventsPlanAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'first_employee', 'event', 'comments') 

    def first_employee(self, obj):
        if obj.employee.exists():
            return obj.employee.first().name
        return 'Сотрудник удалён'
    first_employee.short_description = 'Сотрудник'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "employee":
            kwargs["queryset"] = Staff.objects.filter(actual=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
class MyAdminSite(admin.AdminSite):
    site_title = 'Система учёта МБУ "Музей истории и этнографии"'
    site_header = 'Система учёта МБУ "Музей истории и этнографии"'
    index_title = 'Добро пожаловать в админку'
    

admin_site = MyAdminSite(name='myadmin')
admin_site.register(TimeOff, TimeOffAdmin)
admin_site.register(Categories, CategoriesAdmin)
admin_site.register(Message, MessageAdmin)
admin_site.register(Subscribers, SubscribersAdmin)
admin_site.register(Staff, StaffAdmin)
admin_site.register(Location, LocationAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(EventList,EventListAdmin)
admin_site.register(Events, EventsAdmin)
admin_site.register(FreeVisitors, FreeVisitorsAdmin)
admin_site.register(FreeOrNot, FreeOrNotAdmin)
admin_site.register(EventsPlan, EventsPlanAdmin)
admin_site.register(Group)
admin_site.register(User)