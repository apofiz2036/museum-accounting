from django.shortcuts import render
from .models import Staff, Location, Category, Events, EventList, FreeVisitors, FreeOrNot
from django.db.models import Sum, Count, Q, Case, When

def main(request):
    staff_members = Staff.objects.all()
    location = Location.objects.all()
    category = Category.objects.all()
    events_list = EventList.objects.all()
    free_or_not = FreeOrNot.objects.all()

    events_query = Events.objects.all()
    free_visitors_query = FreeVisitors.objects.all()

    if request.method == 'POST':
        selected_staff_members = request.POST.getlist('staff_members')
        selected_location = request.POST.getlist('location')
        selected_category = request.POST.getlist('category')
        selected_event_list = request.POST.getlist('events_list')
        selected_free_or_not = request.POST.getlist('free_or_not')

        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')

        if selected_staff_members:
            events_query = events_query.filter(employee__id__in=selected_staff_members)
        if selected_location:
            events_query = events_query.filter(location__id__in=selected_location)
        if selected_category:
            events_query = events_query.filter(category__id__in=selected_category)
        if selected_event_list:
            events_query = events_query.filter(event_name__id__in=selected_event_list)
        if selected_free_or_not:
            events_query = events_query.filter(free_or_not__id__in=selected_free_or_not)
            free_visitors_query = events_query.filter(free_or_not__id__in=selected_free_or_not)
        if date_from:
            events_query = events_query.filter(date__gte=date_from)
            free_visitors_query = free_visitors_query.filter(date__gte=date_from)
        if date_to:
            events_query = events_query.filter(date__lte=date_to)
            free_visitors_query = free_visitors_query.filter(date__lte=date_to)
            
    events_aggregate = (
        events_query
        .aggregate(
            vpn_sum=Sum('VPN'),
            adults_sum=Sum('adults'),
            university_students_sum=Sum('university_students'),
            college_students_sum=Sum('college_students'),
            school_sum=Sum('school'),
            children_sum=Sum('children'),
            pensioners_sum=Sum('pensioners'),
            socially_supported_children_sum=Sum('socially_supported_children'),
            socially_supported_adult_sum=Sum('socially_supported_adult'),
            pushkn_cards_sum=Sum('pushkn_cards'),
            indigenous_children_sum=Sum('indigenous_children'),
            indigenous_adult_sum=Sum('indigenous_adult'),
            autism_spectrum_children_sum=Sum('autism_spectrum_children'),
            svo_children_sum=Sum('svo_children'),
            preferential_sum=Sum('preferential'),
            all_sum=Sum('adults') + Sum('university_students') + Sum('college_students') + Sum('school') + Sum('children') + Sum('pensioners'),
            vpn_count=Count(Case(When(VPN__gt=0, then=1))),
            adults_count=Count(Case(When(adults__gt=0, then=1))),
            university_students_count=Count(Case(When(university_students__gt=0, then=1))),
            college_students_count=Count(Case(When(college_students__gt=0, then=1))),
            school_count=Count(Case(When(school__gt=0, then=1))),
            children_count=Count(Case(When(children__gt=0, then=1))),
            pensioners_count=Count(Case(When(pensioners__gt=0, then=1))),
            socially_supported_children_count=Count(Case(When(socially_supported_children__gt=0, then=1))),
            socially_supported_adult_count=Count(Case(When(socially_supported_adult__gt=0, then=1))),
            pushkn_cards_count=Count(Case(When(pushkn_cards__gt=0, then=1))),
            indigenous_children_count=Count(Case(When(indigenous_children__gt=0, then=1))),
            indigenous_adult_count=Count(Case(When(indigenous_adult__gt=0, then=1))),
            autism_spectrum_children_count=Count(Case(When(autism_spectrum_children__gt=0, then=1))),
            svo_children_count=Count(Case(When(svo_children__gt=0, then=1))),
            preferential_count=Count(Case(When(preferential__gt=0, then=1))),
            all_count=Count('*')           
        )
    )

    free_visitors_aggregate = (
        free_visitors_query
        .aggregate(
            vpn_sum=Sum('VPN'),
            adults_sum=Sum('adults'),
            university_students_sum=Sum('university_students'),
            college_students_sum=Sum('college_students'),
            school_sum=Sum('school'),
            children_sum=Sum('children'),
            pensioners_sum=Sum('pensioners'),
            socially_supported_children_sum=Sum('socially_supported_children'),
            socially_supported_adult_sum=Sum('socially_supported_adult'),
            pushkn_cards_sum=Sum('pushkn_cards'),
            indigenous_children_sum=Sum('indigenous_children'),
            indigenous_adult_sum=Sum('indigenous_adult'),
            autism_spectrum_children_sum=Sum('autism_spectrum_children'),
            svo_children_sum=Sum('svo_children'),
            preferential_sum=Sum('preferential'),
            all_sum=Sum('adults') + Sum('university_students') + Sum('college_students') + Sum('school') + Sum('children') + Sum('pensioners'),
            all_count=Count('*') 
        )
    )

    return render(
        request,
        'events/main.html',
        {
            'staff_members': staff_members,
            'location': location,
            'category': category,
            'events_list': events_list,
            'free_or_not': free_or_not,
            'events': events_aggregate,
            'free_visitors': free_visitors_aggregate,
        }
    )
