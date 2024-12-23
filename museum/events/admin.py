from django.contrib import admin
from .models import Staff, Location, Category, EventList, Events, FreeVisitors, FreeOrNot
from .forms import EventForm
from django.utils import formats

class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'actual')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('location',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class EventListAdmin(admin.ModelAdmin):
    list_display = ('event_name',)

class EventsAdmin(admin.ModelAdmin):
    list_display = ('date', 'first_employee', 'location', 'event_name', 'Comments')
    list_filter = ('date', 'employee', 'location', 'event_name', 'category')

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
    
class MyAdminSite(admin.AdminSite):
    site_title = 'Система учёта посетителей МБУ "Музей истории и этнографии"'
    site_header = 'Система учёта посетителей МБУ "Музей истории и этнографии"'
    index_title = 'Добро пожаловать в админку'



admin_site = MyAdminSite(name='myadmin')
admin_site.register(Staff, StaffAdmin)
admin_site.register(Location, LocationAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(EventList,EventListAdmin)
admin_site.register(Events, EventsAdmin)
admin_site.register(FreeVisitors, FreeVisitorsAdmin)
admin_site.register(FreeOrNot, FreeOrNotAdmin)
