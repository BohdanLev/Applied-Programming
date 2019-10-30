from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:ticket_id>/', views.detail, name = 'detail'),
    path('book/<int:ticket_id>', views.book_ticket, name = 'book_ticket'),
    path('buy/<int:ticket_id>', views.buy_ticket, name = 'buy_ticket'),
    path('bookagree/<int:ticket_id>', views.book, name = 'book'),
    path('buyagree/<int:ticket_id>', views.buy, name = 'buy'),
    path('unbook/<int:ticket_id>', views.unbook_ticket, name = 'unbook_ticket'),
    path('buyagree/<int:ticket_id>', views.unbook, name = 'unbook'),
]
