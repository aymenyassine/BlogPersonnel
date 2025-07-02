from django.urls import path
from .views import (
    AmisListAPIView,
    AmisRequestCreateAPIView,
    AmisRequestResponseAPIView,
    AmisDamisAPIView,
    AmisDemandesRecuesAPIView,
    PeopleToFollowView,
    SentInvitationsList,
)
from .views import(
    ChatListAPIView,ChatCreateAPIView,ChatMarkAsReadAPIView,GetAllUsers,ConversationAPIView
)

urlpatterns = [
    path('demandes/<int:user_id>/', AmisRequestCreateAPIView.as_view(), name='amis-request-create'),
    path('demandes/<int:pk>/<str:action>/', AmisRequestResponseAPIView.as_view(), name='friend-request-response'),
    path('mes-amis/', AmisListAPIView.as_view(), name='friend-list'),
    path('amis-damis/<int:user_id>/', AmisDamisAPIView.as_view(), name='amis-autre-utilisateur'),
    path('demandes-recues/', AmisDemandesRecuesAPIView.as_view(), name='demandes-recues'),
    path('suggestions/', PeopleToFollowView.as_view(), name='people-to-follow'),
     path('demandes-envoyees/', SentInvitationsList.as_view(), name='sent-invitations'),
    # Chat url
    path('chat/', ChatListAPIView.as_view(), name='chat-list'),
    path('chat/<int:id_recevoir>/', ChatCreateAPIView.as_view(), name='chat-create'),
    path('chat/read/<int:id_user>/', ChatMarkAsReadAPIView.as_view()),
    path('list_user/',GetAllUsers.as_view(),name='list_user'),
    path('chat/conversation/<int:id_ami>/', ConversationAPIView.as_view(),name='conversation'),

]    