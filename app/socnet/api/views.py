from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from socnet.api.serializers import PostSerializer
from socnet.models import Post, Like
from datetime import datetime, timedelta


class CreatePostView(APIView):

    def post(self, request):
        user = request.user
        data = request.data
        title = data.get('title', None)
        content = data.get('content', None)
        if title is None:
            return Response(
                {"message": 'Request must have key "title".'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if content is None:
            return Response(
                {"message": 'Request must have key "content".'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.is_anonymous:
            return Response(
                {"message": "You haven't logged in."},
                status=status.HTTP_400_BAD_REQUEST
            )
        data['author'] = user.id
        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikePostView(APIView):

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(
                {"message": "Post does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        user = request.user

        if user.is_anonymous:
            return Response(
                {"message": "You haven't logged in."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Like.objects.filter(post=post, user=user).exists():
            return Response(
                {"message": "You have liked this post already."},
                status=status.HTTP_400_BAD_REQUEST
            )

        Like.objects.create(post=post, user=user)
        post.likes_count += 1
        post.save()

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UnlikePostView(APIView):

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(
                {"message": "Post does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        user = request.user

        if user.is_anonymous:
            return Response(
                {"message": "You haven't logged in."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not Like.objects.filter(post=post, user=user).exists():
            return Response(
                {"message": "You have not liked this post yet."},
                status=status.HTTP_400_BAD_REQUEST
            )

        like = Like.objects.filter(post=post, user=user).first()
        like.delete()

        post.likes_count -= 1
        post.save()

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeAnalyticsView(APIView):
    def get(self, request):
        date_from = request.query_params.get('date_from', None)
        date_to = request.query_params.get('date_to', None)

        try:
            date_from = (
                date_from
                if date_from is not None
                else str(datetime.now().date())
            )
            datetime.strptime(date_from, '%Y-%m-%d')
            date_to = (
                date_to
                if date_to is not None
                else str(datetime.now().date())
            )
            datetime.strptime(date_to, '%Y-%m-%d')

        except ValueError:
            return Response(
                {"message": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        start_date = datetime.strptime(date_from, '%Y-%m-%d')
        end_date = datetime.strptime(date_to, '%Y-%m-%d')

        date_likes = {}

        current_date = start_date

        while current_date <= end_date:
            next_date = current_date + timedelta(days=1)
            likes_count = Like.objects.filter(
                created_at__range=(current_date, next_date)
            ).count()

            date_likes[current_date.strftime('%Y-%m-%d')] = likes_count
            current_date = next_date

        return Response(
            {
                'date_from': date_from,
                'date_to': date_to,
                "likes_by_date": date_likes,
            },
            status=status.HTTP_200_OK
        )
