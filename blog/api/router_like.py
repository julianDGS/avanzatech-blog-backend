from rest_framework.routers import DefaultRouter

from blog.api.view_sets_like import LikeViewSet

router = DefaultRouter()

router.register(r'', LikeViewSet, basename='like')

urlpatterns = router.urls