from rest_framework.routers import DefaultRouter

from .view_sets import BlogPostViewSet

router = DefaultRouter()

router.register(r'', BlogPostViewSet, basename='post')

urlpatterns = router.urls