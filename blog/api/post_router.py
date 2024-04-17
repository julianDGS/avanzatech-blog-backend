from rest_framework.routers import DefaultRouter

from .post_view_set import BlogPostViewSet

router = DefaultRouter()

router.register(r'', BlogPostViewSet, basename='post')

urlpatterns = router.urls