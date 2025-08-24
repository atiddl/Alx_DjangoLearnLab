from rest_framework import viewsets, permissions, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Post, Like
from .serializers import PostSerializer
from notifications.models import Notification

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):

        post = get_object_or_404(Post, pk=pk)
        user = request.user

        if Like.objects.filter(post=post, user=user).exists():
            return Response({'detail': 'You already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        Like.objects.create(post=post, user=user)

        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='liked your post',
                target=post
            )

        return Response({'detail': 'Post liked.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        like = Like.objects.filter(post=post, user=user).first()
        if not like:
            return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()

        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='unliked your post',
                target=post
            )

        return Response({'detail': 'Post unliked.'}, status=status.HTTP_200_OK)

class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        followed_users = user.following.all() 
        posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(posts, request)

        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


# from rest_framework import viewsets, permissions, filters, status
# from rest_framework.pagination import PageNumberPagination
# from .models import Post, Comment,Like
# from .serializers import PostSerializer, CommentSerializer, LikeSerializer
# from .permissions import IsAuthorOrReadOnly
# from rest_framework.decorators import api_view, permission_classes,action
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.shortcuts import get_object_or_404
# from notifications.models import Notification


# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 50

# # class PostViewSet(viewsets.ModelViewSet):
# #     queryset = Post.objects.all()
# #     serializer_class = PostSerializer
# #     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# #     @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
# #     def like(self, request, pk=None):
# #         post = self.get_object()
# #         user = request.user

# #         if Like.objects.filter(post=post, user=user).exists():
# #             return Response({'detail': 'You already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

# #         Like.objects.create(post=post, user=user)
# #         # TODO: Create notification for post author here
# #         return Response({'detail': 'Post liked.'}, status=status.HTTP_201_CREATED)

# #     @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
# #     def unlike(self, request, pk=None):
# #         post = self.get_object()
# #         user = request.user

# #         like = Like.objects.filter(post=post, user=user).first()
# #         if not like:
# #             return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

# #         like.delete()
# #         return Response({'detail': 'Post unliked.'}, status=status.HTTP_200_OK)



# class LikePostView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, pk):
#         post = get_object_or_404(Post, pk=pk)
#         like, created = Like.objects.get_or_create(user=request.user, post=post)

#         if created:
#             Notification.objects.create(
#                 recipient=post.author,
#                 actor=request.user,
#                 verb="liked your post",
#                 target=post
#             )
#             return Response({"message": "Post liked."}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"message": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)


# class UnlikePostView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, pk):
#         post = get_object_or_404(Post, pk=pk)
#         try:
#             like = Like.objects.get(user=request.user, post=post)
#             like.delete()
#             Notification.objects.create(
#                 recipient=post.author,
#                 actor=request.user,
#                 verb="unliked your post",
#                 target=post
#             )
#             return Response({"message": "Post unliked."}, status=status.HTTP_200_OK)
#         except Like.DoesNotExist:
#             return Response({"message": "You have not liked this post yet."}, status=status.HTTP_400_BAD_REQUEST)

# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all().order_by('-created_at')
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
#     pagination_class = StandardResultsSetPagination
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['title', 'content']

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

#     @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
#     def like(self, request, pk=None):
#         post = self.get_object()
#         user = request.user
        
#         if Like.objects.filter(post=post, user=user).exists():
#             return Response({'detail': 'You already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

#         like = Like.objects.create(post=post, user=user)
#         return Response({'detail': 'Post liked.'}, status=status.HTTP_201_CREATED)

#     @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
#     def unlike(self, request, pk=None):
#         post = self.get_object()
#         user = request.user
        
#         like = Like.objects.filter(post=post, user=user).first()
#         if not like:
#             return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)
        
#         like.delete()
#         return Response({'detail': 'Post unliked.'}, status=status.HTTP_200_OK)
    
#     @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
#     def like(self, request, pk=None):
#         post = self.get_object()
#         user = request.user
#         if Like.objects.filter(post=post, user=user).exists():
#             return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
#         Like.objects.create(post=post, user=user)

#         # Create a notification for the post author
#         if post.author != user:
#             Notification.objects.create(
#                 recipient=post.author,
#                 actor=user,
#                 verb='liked',
#                 target=post
#             )

#         return Response({'detail': 'Post liked'}, status=status.HTTP_201_CREATED)


# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all().order_by('-created_at')
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
#     pagination_class = StandardResultsSetPagination

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])

# def user_feed(request):
#     user = request.user
#     followed_users = user.following.all()  
#     posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')

#     paginator = PageNumberPagination()
#     paginator.page_size = 10
#     result_page = paginator.paginate_queryset(posts, request)

#     serializer = PostSerializer(result_page, many=True)
#     return paginator.get_paginated_response(serializer.data)


# class FeedView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         following_users = user.following.all()
#         posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)


