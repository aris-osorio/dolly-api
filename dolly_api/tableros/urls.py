from tableros.views import TablerosViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', TablerosViewSet)

urlpatterns = router.urls