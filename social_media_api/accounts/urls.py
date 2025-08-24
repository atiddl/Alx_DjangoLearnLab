from django.urls import path
from .views import RegisterView, LoginView, ProfileView
from .views import FollowUser, UnfollowUser

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', FollowUser, name='follow-user'),
    path('unfollow/<int:user_id>/', unfollowUser, name='unfollow-user'),
]
