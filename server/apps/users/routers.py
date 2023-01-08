from rest_framework.routers import DefaultRouter
from .controllers import UserController


router = DefaultRouter()

router.register(r'', UserController, basename='Users')

urlpatterns = router.urls