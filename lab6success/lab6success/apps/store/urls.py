"""lab6success URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('done/', views.index, name='index'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('get/<ticket_id>/', views.get_ticket_id, name='get_ticket_id'),
    path('inventory/', views.get_all_tickets, name='get_all_tickets'),
    path('order_ticket/', views.order_ticket, name='order_ticket'),
    path('book_ticket/', views.book_ticket, name='book_ticket'),
    path('cancel_book_ticket/',views.cancel_book_ticket,name='cancel_book_ticket'),
    path('get_all_tickets/',views.user_get_all_tickets,name='user_get_all_tickets'),
    path('add_event/',views.add_event,name = 'add_event'),
    path('all/',views.get_events,name = 'get_events'),
    path('<str:event>/tickets/',views.get_event_tickets,name='get_event_tickets')
]
