from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeedView
from .views import PostViewSet, CommentViewSet, LikePostView, UnlikePostView, user_feed

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='user_feed'),
    # path('feed/', user_feed, name='user-feed'),
    path('<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
]

