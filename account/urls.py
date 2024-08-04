from rest_framework.routers import SimpleRouter

from account.views import UserViewSet, RegisterViewSet, LoginViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'user', UserViewSet, basename='user')
router.register(r'register', RegisterViewSet, basename='registration')
router.register(r'login', LoginViewSet, basename='login')
urlpatterns = [
    *router.urls
]