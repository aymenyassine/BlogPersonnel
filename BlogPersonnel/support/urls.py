from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

# urlpatterns = [
#     path('tickets/', views.ticket_list, name='ticket_list'),
#     path('ticket/<int:pk>/', views.ticket_detail, name='ticket_detail'),
# ]


router = DefaultRouter()
router.register(r'tickets', views.TicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls)),
]