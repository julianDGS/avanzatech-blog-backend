from rest_framework.routers import DefaultRouter

from blog.api.like_view_set import LikeViewSet

router = DefaultRouter()

router.register(r'', LikeViewSet, basename='like')

urlpatterns = router.urls