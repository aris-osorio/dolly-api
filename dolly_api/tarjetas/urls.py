from tarjetas.views import TarjetasViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', TarjetasViewSet)

urlpatterns = router.urls