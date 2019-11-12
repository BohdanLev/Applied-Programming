from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from .models import Ticket, TicketStatus, User, Event
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User as usr
import json


@csrf_protect
@csrf_exempt
def index(request):
    return HttpResponse("Done")

@csrf_protect
@csrf_exempt
def get_all_tickets(request):
    if (request.method == "GET"):
        try:
            tickets = Ticket.objects.filter(ticket_status=TicketStatus.AVAILABLE)
        except:
            return HttpResponseBadRequest()
        all = {}
        for ticket in tickets:
            all[str(ticket.id)] = {"nameOfEvent": ticket.ticket_event.name_of_event,
                                   "dateOfEvent": ticket.ticket_event.date_of_event, "price": ticket.ticket_price,
                                   "status": TicketStatus.intToStatus(ticket.ticket_status)}
        return JsonResponse(all)


@csrf_protect
@csrf_exempt
def order_ticket(request):
    if request.method == "POST":
        json_data = json.loads(request.body.decode("utf-8"))
        username = json_data['username']
        password = json_data['password']
        id = json_data['id']
        try:
            user = User.objects.get(user_name=username)
            if user.password != password:
                return HttpResponse("Your username and password didn't match.")
        except:
            return HttpResponse("Please register firstly")
        try:
            ticket = Ticket.objects.get(id=id)
        except:
            raise HttpResponseBadRequest("Error id")
        if ticket.ticket_status == TicketStatus.BOUGHT:
            return HttpResponseBadRequest()
        if ticket.ticket_status == TicketStatus.BOOKED:
            if ticket.ticket_user != user:
                return HttpResponseBadRequest()
        ticket.ticket_status = TicketStatus.BOUGHT
        ticket.ticket_user = user
        ticket.save()
        return HttpResponse("Done")


@csrf_protect
@csrf_exempt
def book_ticket(request):
    if request.method == "POST":
        json_data = json.loads(request.body.decode("utf-8"))
        username = json_data['username']
        password = json_data['password']
        id = json_data['id']
        try:
            user = User.objects.get(user_name=username)
            if user.password != password:
                return HttpResponse("Your username and password didn't match.")
        except:
            return HttpResponse("Please register firstly")
        try:
            ticket = Ticket.objects.get(id=id)
        except:
            raise Http404("Error id")
        if ticket.ticket_status == TicketStatus.BOUGHT or ticket.ticket_status == TicketStatus.BOOKED:
            if ticket.ticket_user == user:
                return HttpResponse("You have already booked")
            return HttpResponseBadRequest()
        ticket.ticket_status = TicketStatus.BOOKED
        ticket.ticket_user = user
        ticket.save()
        return HttpResponse("Done")


@csrf_protect
@csrf_exempt
def cancel_book_ticket(request):
    if request.method == "POST":
        json_data = json.loads(request.body.decode("utf-8"))
        username = json_data['username']
        password = json_data['password']
        id = json_data['id']
        try:
            user = User.objects.get(user_name=username)
            if user.password != password:
                return HttpResponse("Your username and password didn't match.")
        except:
            return HttpResponse("Please register firstly")
        try:
            ticket = Ticket.objects.get(id=id)
        except:
            raise HttpResponseBadRequest("Error id")
        if ticket.ticket_status == TicketStatus.BOUGHT:
            return HttpResponseBadRequest()
        if ticket.ticket_status == TicketStatus.BOOKED and ticket.ticket_user != user:
            return HttpResponseBadRequest()
        ticket.ticket_status = TicketStatus.AVAILABLE
        ticket.ticket_user = None
        ticket.save()
        return HttpResponse("Success")


@csrf_protect
@csrf_exempt
def get_ticket_id(request, ticket_id):
    if request.method == "GET":
        try:
            ticket = Ticket.objects.get(id=int(ticket_id))
        except:
            return HttpResponseBadRequest()
        return JsonResponse({"Name of event": ticket.ticket_event.name_of_event,"date": ticket.ticket_event.date_of_event, "price": ticket.ticket_price,
                             "status": TicketStatus.intToStatus(ticket.ticket_status)})
    return HttpResponse("Good")


@csrf_protect
@csrf_exempt
def user_get_all_tickets(request):
    json_data = json.loads(request.body.decode("utf-8"))
    username = json_data['username']
    password = json_data['password']
    try:
        user = User.objects.get(user_name=username)
        if user.password != password:
            return HttpResponse("Your username and password didn't match.")
    except:
        return HttpResponse("Please register firstly")
    print(user.id)
    try:
        tickets = Ticket.objects.filter(ticket_user_id=user.id)
    except:
        return HttpResponse("Your list is clear")

    all = {}
    i = 1
    for ticket in tickets:
        all[str(i)] = {"id": ticket.id, "nameOfEvent": ticket.ticket_event.name_of_event,
                       "dateOfEvent": ticket.ticket_event.date_of_event,
                       "price": ticket.ticket_price, "status": TicketStatus.intToStatus(ticket.ticket_status)}
        i += 1
    return JsonResponse(all)

@csrf_protect
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        json_data = json.loads(request.body.decode("utf-8"))
        user_name = json_data['username']
        first_name = json_data['firstName']
        last_name = json_data['lastName']
        email = json_data['email']
        password = json_data['password']
        phone = json_data['phone']
        try:
            user = User.objects.get(user_name = user_name)
            return HttpResponseBadRequest()
        except:
            User.objects.create(user_name=user_name, first_name=first_name, last_name=last_name, email=email,
                                password=password, phone=phone)
            return HttpResponse("Successfuly created")


@csrf_protect
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        json_data = json.loads(request.body.decode("utf-8"))
        username = json_data['username']
        password = json_data['password']
        user = None
        try:
            user = User.objects.get(user_name=username)
        except:
            return HttpResponseBadRequest()

        if(user != None):
            if user.password == password:
                #request.session['member_id'] = m.id
                return HttpResponse("You're logged in.")
            else:
                return HttpResponseBadRequest()


@csrf_protect
@csrf_exempt
def get_events(request):
    if request.method == "GET":
        try:
            events = Event.objects.all()
        except:
            return HttpResponse("No available tickets")
        all = {}
        for event in events:
            all[str(event.id)] = {"nameOfEvent": event.name_of_event,
                                  "dateOfEvent": event.date_of_event}
        return JsonResponse(all)


@csrf_protect
@csrf_exempt
def get_event_tickets(request, event):
    if request.method == "GET":
        try:
            event = Event.objects.get(name_of_event=event)
            tickets = Ticket.objects.filter(ticket_event=event)
        except:
            return HttpResponseBadRequest()
        all = {}
        for ticket in tickets:
            all[str(ticket.id)] = {"nameOfEvent": event.name_of_event,
                                   "dateOfEvent": event.date_of_event,
                                   "price": ticket.ticket_price,
                                   "status": TicketStatus.intToStatus(ticket.ticket_status)}
        return JsonResponse(all)


@csrf_protect
@csrf_exempt
def add_event(request):
    try:
        json_data = json.loads(request.body.decode("utf-8"))
        name_of_event = json_data['name']
        date_of_event = json_data['date']
    except:
        return HttpResponseBadRequest()
    if request.method == "POST":
        Event.objects.create(name_of_event=name_of_event, date_of_event=date_of_event)
        event = Event.objects.get(name_of_event=name_of_event, date_of_event=date_of_event)
        event.add_tickets(100, 250)
    return HttpResponse("Success")
