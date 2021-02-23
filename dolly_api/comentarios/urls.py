from comentarios.views import ComentariosViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', ComentariosViewSet)

urlpatterns = router.urls