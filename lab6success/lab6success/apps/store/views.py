
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from .models import Ticket,TicketStatus, User
from django.http import JsonResponse
import json

@csrf_protect
@csrf_exempt
def index(request):
    return HttpResponse("Done")


@csrf_protect
@csrf_exempt
def new_ticket(request):
    if request.method == "POST":
        json_data = json.loads(request.body.decode("utf-8"))
        name_of_event = json_data['nameOfEvent']
        date = json_data['date']
        ticket_price = json_data['ticketPrice']
        status = json_data['status']
        available_status = ["bought", "booked", "available"]
        if status not in available_status:
            return HttpResponseBadRequest()
        Ticket.objects.create(ticket_name_of_event=name_of_event, ticket_date_of_event=date, ticket_price=ticket_price,
                              ticket_status=TicketStatus.statusToInt(status),ticket_user=None,)
    return HttpResponse("Done")


@csrf_protect
@csrf_exempt
def get_all_tickets(request):
    if(request.method == "GET"):
        try:
            tickets = Ticket.objects.filter(ticket_status=TicketStatus.AVAILABLE)
        except:
            return HttpResponseBadRequest()
        all = {}
        for ticket in tickets:
            all[str(ticket.id)] = {"nameOfEvent": ticket.ticket_name_of_event,"dateOfEvent": ticket.ticket_date_of_event,"price": ticket.ticket_price,"status": TicketStatus.intToStatus(ticket.ticket_status)}
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
            raise Http404("Error id")
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
            raise Http404("Error id")
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
def get_ticket_id(request,ticket_id):
    if request.method == "GET":
        try:
            ticket = Ticket.objects.get(id = int(ticket_id))
        except:
            return HttpResponseBadRequest()
        return JsonResponse({"nameOfEvent": ticket.ticket_name_of_event,"dateOfEvent": ticket.ticket_date_of_event,"price": ticket.ticket_price,"status": TicketStatus.intToStatus(ticket.ticket_status)})
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
        all[str(i)] = {"id": ticket.id, "nameOfEvent": ticket.ticket_name_of_event, "dateOfEvent": ticket.ticket_date_of_event,
                               "price": ticket.ticket_price, "status": TicketStatus.intToStatus(ticket.ticket_status)}
        i+=1
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