from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('post/', include(('blog.api.post_router', 'blog.api'), namespace='posts')),
    path('like/', include(('blog.api.like_router', 'blog.api'), namespace='likes')),
]
