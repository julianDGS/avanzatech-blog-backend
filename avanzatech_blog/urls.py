from django.contrib import admin
from django.urls import path, include
from user.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('post/', include(('blog.api.post_router', 'blog.api'), namespace='posts')),
    path('like/', include(('blog.api.like_router', 'blog.api'), namespace='likes')),
    path('comment/', include(('blog.api.comment_router', 'blog.api'), namespace='comments')),
    path('permission/', include('permission.urls')),
    path('', login_view)
]
