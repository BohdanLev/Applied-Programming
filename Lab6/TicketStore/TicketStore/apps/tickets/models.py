from django.db import models
from django_enumfield import enum

class TicketStatus(enum.Enum):
    BOUGHT = 0
    BOOKED = 1
    AVAILABLE = 2

class Ticket(models.Model):
    ticket_name_of_event = models.CharField('Name of event', max_length = 200)
    ticket_date_of_event = models.DateTimeField('Date of event')
    ticket_price = models.IntegerField()
    ticket_status = enum.EnumField(TicketStatus, default=TicketStatus.AVAILABLE)

    def __str__(self):
        return self.ticket_name_of_event
    pass

class User(models.Model):
    user_name = models.CharField('Name of user', max_length = 50)
    number_phone = models.CharField('Number of phone', max_length = 12)
    ticket_booked = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_name
    pass
