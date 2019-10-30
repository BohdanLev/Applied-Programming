from django.shortcuts import render
from .models import Ticket, TicketStatus, User
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse

def index(request):
    new_ticket_list = Ticket.objects.order_by('-ticket_date_of_event')
    return render(request, 'tickets/list.html', {'new_ticket_list': new_ticket_list})

def detail(request, ticket_id):
    try:
        a = Ticket.objects.get(id = ticket_id)
    except:
        raise Http404("Ticket not Found")

    return render(request, 'tickets/detail.html', {'ticket': a})

def book_ticket(request, ticket_id):
    try:
        a = Ticket.objects.get(id = ticket_id)
    except:
        raise Http404("Ticket not Found")

    return render(request, 'tickets/bookstore.html', {'ticket': a})

def buy_ticket(request, ticket_id):
    try:
        a = Ticket.objects.get(id = ticket_id)
    except:
        raise Http404("Ticket not Found")

    return render(request, 'tickets/buystore.html', {'ticket': a})
    pass

def book(request, ticket_id):
    try:
        a = Ticket.objects.get(id = ticket_id)
    except:
        raise Http404("Ticket not Found")
    if a.ticket_status == TicketStatus.BOOKED:
        return HttpResponse("Ticket already booked")
    if a.ticket_status == TicketStatus.BOUGHT:
        return HttpResponse("Ticket already bought")

    a.ticket_status = TicketStatus.BOOKED
    a.save()

    try:
        user = User.objects.get(number_phone = request.POST['phone'])
        a.user_set.add(user)
    except:
        user = User.objects.create(user_name = request.POST['name'], number_phone = request.POST['phone'], ticket_booked = a)

    return HttpResponseRedirect(reverse('index'))

def buy(request, ticket_id):
    try:
        a = Ticket.objects.get(id = ticket_id)
    except:
        raise Http404("Ticket not Found")
    if a.ticket_status == TicketStatus.BOUGHT:
        return HttpResponse("Ticket already bought")

    a.ticket_status = TicketStatus.BOUGHT

    try:
        user = User.objects.get(number_phone = request.POST['phone'])
    except:
        user = User.objects.create(user_name = request.POST['name'], number_phone = request.POST['phone'], ticket_booked = a)

    a.delete()

    return HttpResponseRedirect(reverse('index'))

def unbook_ticket(request, ticket_id):
    try:
        a = Ticket.objects.get(id = ticket_id)
    except:
        raise Http404("Ticket not Found")

    if a.ticket_status != TicketStatus.BOOKED:
        return HttpResponse("Error!!!")
    else:
        return render(request, 'tickets/unbookstore.html', {'ticket': a})

def unbook(request, ticket_id):
    try:
        a = Ticket.objects.get(id = ticket_id)
    except:
        raise Http404("Ticket not Found")

    try:
        user = User.objects.get(number_phone = request.POST['phone'], user_name = request.POST['name'])
    except:
        return HttpResponse("Error!!!")

    if user.ticket_booked.id == a.id:
        Ticket.objects.create(ticket_name_of_event = a.ticket_name_of_event,
                              ticket_price = a.ticket_price,
                              ticket_date_of_event = a.ticket_date_of_event,
                              ticket_status = TicketStatus.AVAILABLE)

        a.delete()
    else:
        Http404("error")

    return HttpResponseRedirect(reverse('index'))
