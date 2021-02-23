from rest_framework.routers import DefaultRouter
from usuarios.views import UsuariosViewSet


router = DefaultRouter()
router.register(r'', UsuariosViewSet)

urlpatterns = router.urls