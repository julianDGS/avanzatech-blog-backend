from rest_framework.routers import DefaultRouter

from blog.api.comment_view_set import CommentViewSet

router = DefaultRouter()

router.register(r'', CommentViewSet, basename='like')

urlpatterns = router.urls