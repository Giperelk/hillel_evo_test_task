from django.urls import path
from socnet.api.views import CreatePostView, LikePostView, UnlikePostView, LikeAnalyticsView

urlpatterns = [
    path('post/create/', CreatePostView.as_view(), name='api-socnet-post-create'),
    path('post/<int:post_id>/like/', LikePostView.as_view(), name='api-socnet-post-like'),
    path('post/<int:post_id>/unlike/', UnlikePostView.as_view(), name='api-socnet-post-unlike'),
    path('analytics/', LikeAnalyticsView.as_view(), name='api-socnet-analytics'),
]
