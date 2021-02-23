from listas.views import ListasViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', ListasViewSet)

urlpatterns = router.urls