# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('post/new/', views.post_create, name='post_create'),
#     path('post/<int:pk>/', views.post_detail, name='post_detail'),
#     path('post/like/<int:pk>', views.like_post, name='like_post'),
#     path('post/signaler/<int:pk>', views.signaler_post, name='signaler_post'),
#     path('post/modifier/<int:id>', views.Postmodifier.as_view(), name='modifier_post'),
#     path('post/supprimer/<int:id>', views.PostSupprimer.as_view(), name='supprimer_post'),
#     path('profile/', views.profile_view, name='profile'),
#     path('profile/<int:user_id>/', views.profile_view, name='profile_id'),
#     path('notification/mark/', views.mark_notifications_as_read, name='mark_notification_as_read'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post-list'),  # Liste et création de posts
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),  # Détail d'un post (incluant l'action de like)
    path('posts/<int:pk>/like/', views.PostLike.as_view(), name='post-like'),  # Aimer un post
    path('posts/<int:post_pk>/comments/', views.CommentList.as_view(), name='comment-list'),  # Liste des commentaires pour un post
    path('notifications/', views.NotificationList.as_view(), name='notification-list'),  # Notifications
    path('categories/', views.CategoryList.as_view(), name='category-list'),  # Liste des catégories
    path('categories/<int:pk>/',views.CategoryType.as_view(),name='categorie-id'),
    path('signaler/', views.SignalerList.as_view(), name='signaler-list'),  # Liste et création de signalements
    path('trends/', views.TopTrendsView.as_view(), name='top-trends'),
    path('topics/', views.TopicsForYouView.as_view(), name='topics-for-you'),
]
