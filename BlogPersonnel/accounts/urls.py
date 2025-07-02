from django.urls import path
# from . import views
from .views import *



# urlpatterns = [
#     path('register/',views.register,name='register'),
#     path('login/',views.login_view,name='login'),
#     path('logout/',views.logout_view,name='logout'),
# ]

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api-register'),
    path('login/', CustomAuthToken.as_view(), name='api-login'),
    path('logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('user/', GetAuthenticatedUser.as_view(), name='get-auth-user'),
    path('update/', UpdateProfileView.as_view(), name='user-update'),
    path('users/',GetAllUsers.as_view(),name='get-all-users'),
    path('user/<int:pk>/',UserProfileView.as_view(),name='get-users'),
    path('user/stats/', UserStatsAPIView.as_view(), name='user-stats'),
    path('user/<int:pk>/',GetUser.as_view(),name='get-user'),
    path('user/stats/', UserStatsAPIView.as_view(), name='user-stats'),
    path('user/posts/views/', UserPostViewsAPIView.as_view(), name='user-post-views'),
    path('user/posts/top-viewed/', UserTopViewedPostsAPIView.as_view(), name='user-top-viewed-posts'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),
]