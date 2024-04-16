from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('post/', include(('blog.api.router_post', 'blog.api'), namespace='posts')),
    path('like/', include(('blog.api.router_like', 'blog.api'), namespace='likes')),
]
