from django.urls import path
from . import views
from .feeds import LatestPostsFeed
from .views import (PostListView,
                    
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView
                    )

urlpatterns = [
    path('', PostListView, name='blog-home'),
    path('tag/<slug:tag_slug>/',views.PostListView, name='post_list_by_tag'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:post_id>/', views.post_detail, name='post-detail'), #learn
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), #learn
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), #learn
    path('about/',views.about, name='blog-about'),
    path('blog/feed/', LatestPostsFeed(), name='post_feed')
    
]