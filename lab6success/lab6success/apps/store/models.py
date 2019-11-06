from django.db import models
from django_enumfield import enum
import json


class User(models.Model):
    user_name = models.CharField("username",max_length=100)
    first_name = models.CharField("First Name", max_length=100)
    last_name = models.CharField("Last Name", max_length=100)
    email = models.CharField("Email", max_length=100)
    password = models.CharField("Password", max_length=100)
    phone = models.CharField("Phone", max_length=100)


class TicketStatus(enum.Enum):
    BOUGHT = 0
    BOOKED = 1
    AVAILABLE = 2

    @staticmethod
    def statusToInt(st):
        if st == "bought":
            return 0
        elif st == "booked":
            return 1
        else:
            return 2

    @staticmethod
    def intToStatus(st):
        if st == 0:
            return "bought"
        elif st == 1:
            return "booked"
        else:
            return "available"


class Ticket(models.Model):
    ticket_name_of_event = models.CharField('Name of event', max_length=200)
    ticket_date_of_event = models.DateTimeField('Date of event')
    ticket_price = models.IntegerField()
    ticket_status = enum.EnumField(TicketStatus, default=TicketStatus.AVAILABLE)
    ticket_user = models.ForeignKey(User, on_delete = models.CASCADE,null=True)

